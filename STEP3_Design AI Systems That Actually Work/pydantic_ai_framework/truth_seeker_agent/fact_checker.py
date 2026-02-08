from pydantic import BaseModel, Field
from enum import Enum
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from config import SYSTEM_PROMPT
from dotenv import load_dotenv
from ddgs import DDGS


load_dotenv()

class Verdict(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNCERTAIN = "uncertain"


class FactCheckerResult(BaseModel):
    claim: str = Field(description="The original text the user submitted")
    verdict: Verdict = Field(description="The verdict on the claim")
    evidence: str = Field(description="A short summary of why it reached that verdict")
    source_url: str = Field(description="The URL of the source that provided the evidence. Must start with http or https.")

class AgentContext(BaseModel):
    search_count: int = 0

# --- 2. The Validator Function ---
# Notice: ctx is RunContext[None] because we don't need to inject a DB or User ID.
# Notice: The arguments MATCH the fields of the FactCheckerResult model!
def verify_evidence(
    ctx: RunContext[None], 
    claim: str, 
    verdict: Verdict, 
    evidence: str, 
    source_url: str
) -> FactCheckerResult:
    
    # Logic 1: Handle Uncertainty
    if verdict == Verdict.UNCERTAIN:
        return FactCheckerResult(
            claim=claim,
            verdict=Verdict.UNCERTAIN,
            evidence="Insufficient data found to verify claim.",
            source_url="" # Empty URL is allowed for uncertain
        )

    # Logic 2: Validate Source URL for definitive answers
    valid_starts = ("http", "https") # Python startswith expects a tuple
    if not source_url.startswith(valid_starts):
        raise ModelRetry("You must provide a valid source URL starting with 'http' or 'https' for definitive verdicts.")

    # Logic 3: Happy Path
    return FactCheckerResult(
        claim=claim,
        verdict=verdict,
        evidence=evidence,
        source_url=source_url
    )

agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt=SYSTEM_PROMPT,
    deps_type=AgentContext,
    output_type=verify_evidence,
    instructions="Search DuckDuckGo for evidence to support or refute the claim."
)

my_session_context = AgentContext()

# We use @agent.tool_plain because we don't need User Context for a search.
@agent.tool
def search_web(ctx: RunContext[AgentContext], query: str) -> str:
    """
    Search DuckDuckGo for the given query.
    Returns the top 5 results as a string.
    """
    if ctx.deps.search_count >= 1:
        return "SYSTEM ERROR: Search limit exceeded. You must make a decision now based on what you have."

    print(ctx.deps.search_count)
    ctx.deps.search_count += 1

    print(f"🔎 Searching for: {query}")
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
        # Combine results into a readable string for the LLM
        return "\n\n".join(
            f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results
        )


if __name__ == "__main__":
    print("⏳ Agent is thinking...")
    try:
        result = agent.run_sync("The earth is flat.", deps=my_session_context)
        print("\n✅ RESULT FOUND:")
        print(f"search count: {my_session_context.search_count}")
        print(f"user claim: {result.output.claim}")
        print(f"Verdict: {result.output.verdict}")
        print(f"Evidence: {result.output.evidence}")
        print(f"Source:  {result.output.source_url}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

