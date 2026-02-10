from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- Models ---
class EmailDraft(BaseModel):
    original_mail: str = Field(description="The original raw text")
    subject: str = Field(description="The subject line")
    body: str = Field(description="The drafted body text")

class EmailCritique(BaseModel):
    score: int = Field(description="Score 1-10", ge=1, le=10)
    feedback: str = Field(description="Specific criticism of tone and content")
    suggestions: list[str] = Field(description="Bullet points on how to improve it")

class FinalEmail(BaseModel):
    subject: str = Field(description="The final subject")
    body: str = Field(description="The final, polished body")

# --- Agent ---
# We don't set a result_type here because we override it dynamically!
editor_agent = Agent(
    'openai:gpt-5-nano',
    system_prompt="You are a professional executive editor. Your goal is to improve communication."
)

def main():
    raw_input = "Give me a refund NOW! Your product sucks!"
    
    # STEP 1: DRAFT
    # We ask the model to structure the raw input
    print(f"\n--- 1. Drafting ---")
    draft_result = editor_agent.run_sync(
        f"Convert this raw text into a proper email draft: '{raw_input}'", 
        output_type=EmailDraft
    )
    draft = draft_result.output
    print(f"Draft Body: {draft.body}")

    # STEP 2: CRITIQUE
    # We send the DRAFT to get a CRITIQUE
    print(f"\n--- 2. Critiquing ---")
    critique_result = editor_agent.run_sync(
        f"Critique this email body for professionalism: '{draft.body}'",
        output_type=EmailCritique
    )
    critique = critique_result.output
    print(f"Score: {critique.score}/10")
    print(f"Feedback: {critique.feedback}")

    # STEP 3: REFINE
    # CRITICAL FIX: We send BOTH the DRAFT and the CRITIQUE
    print(f"\n--- 3. Refining ---")
    final_result = editor_agent.run_sync(
        f"Rewrite this email body: '{draft.body}' \n\nBased on this feedback: '{critique.feedback}'",
        output_type=FinalEmail
    )
    final = final_result.output
    
    print("\n" + "="*30)
    print(f"FINAL SUBJECT: {final.subject}")
    print(f"FINAL BODY:\n{final.body}")
    print("="*30)

if __name__ == "__main__":
    main()