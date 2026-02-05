"""
Example: 09_pydanticai_dependency_injection.py
Purpose: Demonstrates how to inject runtime data (Context) into an Agent using PydanticAI.

KEY CONCEPTS EXPLAINED:

1. Dependencies (`deps`):
   - The "Fuel" for the Agent.
   - In Vanilla OpenAI, you usually format strings manually (e.g., f"User: {user.name}").
   - In PydanticAI, you define a structure (class) for this data and "inject" it when you run the agent.
   - This separates the Logic (Agent) from the Data (User/Request), allowing one Agent to serve thousands of concurrent users safely.

2. RunContext (`ctx`):
   - The "Bridge" or "Wrapper".
   - Functions like system prompts or tools don't automatically know about your data.
   - `RunContext` wraps your dependency object so it can be passed into these functions.
   - You access your data via `ctx.deps`.

3. Dynamic System Prompts (`@agent.system_prompt`):
   - Instead of a static string ("You are a helpful assistant"), this is a function that runs *just in time* before the LLM call.
   - It allows you to build a custom persona based on the specific user calling the agent.

4. Dataclasses:
   - Used here as a lightweight container for the dependency data.
   - You could also use Pydantic `BaseModel` if you needed strict validation on the input data.
"""

from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# 1. DEFINE THE CONTEXT STRUCTURE (The Fuel Tank)
# ============================================================================
# We use a dataclass to define what kind of data this agent NEEDS to run.
# This acts as a contract: "I cannot run unless you give me a User object."
@dataclass
class User:
    name: str

# ============================================================================
# 2. DEFINE THE AGENT (The Engine)
# ============================================================================
# deps_type=User tells the agent: "Expect a 'User' object when run."
agent = Agent(
    model="gpt-5-nano",
    deps_type=User
)

# ============================================================================
# 3. DEFINE DYNAMIC PROMPTS (The Logic)
# ============================================================================
# This function runs automatically every time the agent is called.
# It uses `ctx` to reach into the injected data (`deps`) and pull out the name.
@agent.system_prompt
def add_name(ctx: RunContext[User]):
    return f"The user name is {ctx.deps.name}. Be nice to them!"

# ============================================================================
# 4. EXECUTION (Injecting the Fuel)
# ============================================================================
# We create the specific data instance (Daniel) and pass it into the run command.
# This is "Dependency Injection" at runtime.
if __name__ == "__main__":
    result = agent.run_sync("Hello!", deps=User(name="Daniel"))
    print(result.output)