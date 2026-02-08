"""
Smart Credit Limit Agent
========================

This module implements a robust, production-grade AI agent responsible for approving or rejecting 
credit limit increase requests. It is designed with a "Safety-First" architecture, prioritizing 
deterministic business logic over LLM improvisation.

Architecture: The "Swiss Cheese" Safety Model
---------------------------------------------
This agent uses a multi-layered approach to safety and compliance, ensuring that no single point 
of failure (like an LLM hallucination) can result in a violation of financial policy.

1.  **Layer 1: The Persona (System Prompt)**
    -   Sets the "friendly and polite" tone.
    -   Provides the LLM with the high-level rules of the road.
    -   *Implementation:* `config.SYSTEM_PROMPT` and dynamic context injection.

2.  **Layer 2: Structural Integrity (Pydantic Models)**
    -   Enforces strict data types for inputs and outputs.
    -   Prevents "stringly typed" errors by using Enums for `RiskProfile` and `Decision`.
    -   *Implementation:* `UserFinancialProfile` and `CreditDecision` classes.

3.  **Layer 3: The Overlord Validator (Python Logic)**
    -   The final line of defense. It is a deterministic Python function that acts as a gatekeeper.
    -   It recalculates the math (Utilization % and Income Limits) independently of the LLM.
    -   **Rule:** If the LLM proposes an action that violates policy (e.g., approving a High Risk user),
        this layer strictly overrides the decision to `REJECTED`.
    -   *Implementation:* `verify_credit_logic` function.

Key Features
------------
* **Dependency Injection:** The database connection is injected into the user profile (`db_connection`), 
    avoiding global state and making the agent fully testable and thread-safe.
* **Context-Aware Tooling:** The `get_monthly_spending` tool pulls data dynamically using the 
    injected DB connection, forcing the agent to perform a "lookup" action.
* **Hybrid Reasoning:** The Validator preserves the LLM's natural reasoning when the decision is 
    correct but enforces a hardcoded "Policy Violation" message when the LLM is wrong.

Usage
-----
Run this script directly to test the agent with a mock scenario:
    $ python credit_agent.py

Dependencies
------------
-   pydantic_ai
-   pydantic
-   python-dotenv
"""

from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic import BaseModel, Field
from enum import Enum
from dotenv import load_dotenv
import config

load_dotenv()

class RiskProfile(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Decision(str, Enum):
    APPROVED = "approve"
    REJECTED = "reject"

class UserFinancialProfile(BaseModel):
    user_id: int = Field(description="The user's ID")
    annual_income: float = Field(description="The user's income in USD. Must be positive and non-zero.")
    current_limit: float = Field(description="The user's current credit limit in USD")
    risk_profile: RiskProfile = Field(description="The user's risk profile")
    db_connection: dict = Field(exclude=True) # Hidden from LLM, used by tools

class CreditDecision(BaseModel):
    decision: Decision = Field(description="The decision on the credit limit")
    new_limit: float = Field(description="The new credit limit in USD")
    reasoning: str = Field(description="The reasoning for the decision")

mock_db = {
    1: {
        "avg_monthly_spend": 1000
    }
}

def verify_credit_logic(ctx: RunContext[UserFinancialProfile], decision: Decision, reasoning: str, new_limit: float, avg_monthly_spend: float) -> CreditDecision:
    if ctx.deps.risk_profile == RiskProfile.HIGH:
        return CreditDecision(
            decision=Decision.REJECTED,
            reasoning="Policy Violation: High Risk Profile.",
            new_limit=ctx.deps.current_limit
        )

    utilization = avg_monthly_spend / ctx.deps.current_limit
    max_income_limit = ctx.deps.annual_income * 0.15

    if utilization < 0.3:
        # if agent tried to approve, we stop him
        if decision == Decision.APPROVED:
            return CreditDecision(
                decision=Decision.REJECTED,
                reasoning=f"Utilization ({utilization:.0%}) is below the 30% threshold.",
                new_limit=ctx.deps.current_limit
            )
        # if agent rejected correctly, we accept its reasoning
        # this keeps the ai voice when the ai is right
        return CreditDecision(
            decision=Decision.REJECTED,
            reasoning=reasoning,
            new_limit=ctx.deps.current_limit
        )

    if new_limit > max_income_limit:
        if decision == Decision.APPROVED:
            return CreditDecision(
                decision=Decision.REJECTED,
                reasoning=f"Requested limit exceeds 15% of annual income (Max: ${max_income_limit}).",
                new_limit=ctx.deps.current_limit
            )

        return CreditDecision(
            decision=Decision.REJECTED,
            reasoning=reasoning,
            new_limit=ctx.deps.current_limit
        )

    # Happy path
    return CreditDecision(
        decision=decision,
        reasoning=reasoning,
        new_limit=new_limit
    )

    


agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt=config.SYSTEM_PROMPT,
    output_type=verify_credit_logic
)

@agent.system_prompt
def add_user_context(ctx: RunContext[UserFinancialProfile]):
    return f"""
        You are a credit limit agent. You are responsible for deciding whether to approve or reject a credit limit increase for a user.
        You will be given a user's financial profile and a request to increase their credit limit.
        You must reponse the user in a friendly and polite tone.

        CURRENT USER DETAILS:
        - User ID: {ctx.deps.user_id}
        - Annual Income: {ctx.deps.annual_income}
        - Current Limit: {ctx.deps.current_limit}
        - Risk Profile: {ctx.deps.risk_profile}

        RULES:
        1. If the user's risk profile is high, you must reject the request and provide suggestions for improving the user's risk profile.
        2. If the user's utilization is below 30%, you must reject the request and provide suggestions for improving the user's utilization.
        3. If the requested limit is greater than 15% of the user's annual income, you must reject the request and provide suggestions for improving the user's annual income.
        4. If the request is approved, you must return the new limit and congratulate the user for their good credit history.
    """

@agent.tool
def get_monthly_spending(ctx: RunContext[UserFinancialProfile]):
    # Access DB via context, not global
    return ctx.deps.db_connection.get(ctx.deps.user_id)



if __name__ == "__main__":
    result = agent.run_sync(
        user_prompt="Increase the credit limit for user 1 to $10,000",
        deps=UserFinancialProfile(user_id=1, annual_income=100000, current_limit=5000, risk_profile=RiskProfile.LOW, db_connection=mock_db)
    )    
    #print(result.output)

    print(f"Model decision: {result.output.decision}")
    print(f"Model reasoning: {result.output.reasoning}")
    print(f"Model new limit: {result.output.new_limit}")

    # NOTE: show the tool calls for this message to verify what the model actually did
    for msg in result.new_messages():
        if msg.parts:
            for part in msg.parts:
                if part.part_kind == "tool-call":
                    print(f"Tool called: {part.tool_name}")







