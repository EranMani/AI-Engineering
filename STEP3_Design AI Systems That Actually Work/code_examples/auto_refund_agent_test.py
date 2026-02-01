import asyncio
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ModelRetry, UnexpectedModelBehavior

# --- 1. THE BACKPACK (Dependency Injection) 🎒 ---
# This holds the context for the CURRENT user request.
# In a real app, this comes from your API/Database.
@dataclass
class SupportContext:
    user_id: str
    user_name: str
    is_premium_member: bool
    request_date: date

# --- 2. THE FORM (Structured Output) 📝 ---
# We force the LLM to fill out this form. No "chatty" text allowed.
class RefundDecision(BaseModel):
    decision: str = Field(description="APPROVE, REJECT, or ESCALATE")
    refund_amount: float
    reason: str = Field(description="Short explanation for the customer")
    manager_check_needed: bool

# --- 3. THE AGENT SETUP 🤖 ---
agent = Agent(
    'openai:gpt-4o',
    deps_type=SupportContext,    # Expects this backpack
    result_type=RefundDecision,  # Forces this output
    system_prompt="You are a refund processing agent. Follow company policy strictly."
)

# --- 4. DYNAMIC PROMPT (Context Injection) 💉 ---
@agent.system_prompt
def add_policy_context(ctx: RunContext[SupportContext]) -> str:
    # We change the rules based on who the user is!
    if ctx.deps.is_premium_member:
        return f"User {ctx.deps.user_name} is a PREMIUM member. Be generous with return windows."
    return f"User {ctx.deps.user_name} is a standard member. Stick strictly to the 30-day rule."

# --- 5. THE TOOL (The Hands) 🛠️ ---
@agent.tool
def verify_order_eligibility(ctx: RunContext[SupportContext], order_id: str, purchase_date: date) -> str:
    """Check if an order is eligible for return based on dates."""
    
    # Self-Correction: Handle bad input formats
    if not order_id.startswith("ORD-"):
        raise ModelRetry("Order IDs must start with 'ORD-'. Please fix and retry.")
    
    # Business Logic
    days_passed = (ctx.deps.request_date - purchase_date).days
    
    # Premium members get 60 days, others get 30
    limit = 60 if ctx.deps.is_premium_member else 30
    
    if days_passed > limit:
        return f"REJECT: Purchase was {days_passed} days ago (Limit is {limit})."
    
    return "ELIGIBLE: Within return window."

# --- 6. RUNNING IT (Production Simulation) 🏃‍♂️ ---
async def main():
    ctx = SupportContext(
        user_id="u_123",
        user_name="Alice", 
        is_premium_member=False,
        request_date=date(2023, 11, 1)
    )

    query = "I bought order 123..." # The "bad" query

    try:
        result = await agent.run(query, deps=ctx)
        
        # Success! 🟢
        print(f"Decision: {result.data.decision}")
        print(f"Reason:   {result.data.reason}")

    except UnexpectedModelBehavior as e:
        # Failure (Safety Net) 🔴
        print(f"[Alert] Agent failed: {e}")
        
        # FALLBACK: Return a safe default so the UI doesn't break
        fallback = RefundDecision(
            decision="ESCALATE",
            refund_amount=0.0,
            reason="I'm having trouble processing this request. Connecting you to a human agent.",
            manager_check_needed=True
        )
        print(f"Fallback Decision: {fallback.decision}")
        print(f"Fallback Reason:   {fallback.reason}")

if __name__ == "__main__":
    asyncio.run(main())