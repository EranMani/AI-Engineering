from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from enum import Enum
from typing import Literal
import logfire
from datetime import datetime

load_dotenv()

logfire.configure()
logfire.instrument_pydantic_ai()

class LoyaltyTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

class Decision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATE = "ESCALATE"

class UserProfile(BaseModel):
    id: int = Field(description="The user's ID")
    name: str = Field(description="The user's name")
    loyalty_tier: LoyaltyTier = Field(description="gold tier can get instant refund for any item under 100$ without checking \
                                                   eligibility. silver tier get refunds up to 50$ but eligibility must always be checked.\
                                                   bronze tier always require eligibility checks and manual approval for anything over $20.")

class RefundDecision(BaseModel):
    decision: Decision = Field(description="The decision on the refund")
    refund_amount: float = Field(description="The amount of the refund. 0.0$ if rejected")
    reasoning: str = Field(description="A short reasoning for the decision")

system_prompt = """
You are a refund agent for a company that sells products online.
Your task is to verify the eligibility of a refund request based on the user's loyalty tier.
if the user is a gold tier - he can get instant refund for any item under 100$ without checking eligibility
if the user is a silver tier - he can get refunds up to 50$ but eligibility must always be checked
if the user is a bronze tier - he always require eligibility checks and manual approval for anything over $20
"""

orders_db = {
    "order123": {
        "items": ["item1", "item2", "item3"],
        "price": 95.0,
        "date": "2026-01-01"
    }
}

# Define the Output Function (The "Final Tool")
def verify_refund_logic(ctx: RunContext[UserProfile], decision: Decision, refund_amount: float, reasoning: str, date_of_purchase: str) -> RefundDecision:
    
    # --- DEBUG PRINTS (Use -s to see these) ---
    print(f"\n🔍 DEBUG: Validator called!")
    print(f"   -> Input Decision: {decision}")
    print(f"   -> Input Date: {date_of_purchase}")
    
    # 1. Parse Date & Calculate Duration
    purchase_date_obj = datetime.strptime(date_of_purchase, "%Y-%m-%d")
    days_passed = (datetime.now() - purchase_date_obj).days
    print(f"   -> Days Passed: {days_passed}")

    # 2. THE LOGIC CHECK
    # We only raise an error if the order is OLD (>30 days) AND the agent tried to APPROVE it.
    is_old = days_passed > 30
    is_approving = (decision == Decision.APPROVED)
    
    if is_old and is_approving:
        print("   ❌ BLOCKING: Order is old and Agent tried to APPROVE. Raising error.")
        #raise ModelRetry("This order is too old to be refunded. Please contact customer support.")
    
    print("   ✅ PASS: Date check OK.")

    # ... The rest of your Bronze/Silver logic goes here ...
    # Rule: Bronze users cannot be APPROVED for > $20
    if ctx.deps.loyalty_tier == LoyaltyTier.BRONZE:
        if decision == Decision.APPROVED and refund_amount > 20.0:
            raise ModelRetry(f"Bronze users cannot be APPROVED for amounts over $20. You must ESCALATE this request.")

    # Rule: Rejected refunds must have 0.0 amount
    if decision == Decision.REJECTED and refund_amount > 0:
        raise ModelRetry("If the decision is REJECTED, the refund_amount must be 0.0.")

    return RefundDecision(
        decision=decision, 
        refund_amount=refund_amount, 
        reasoning=reasoning
    )

agent = Agent(
    model="gpt-5-nano",
    deps_type=UserProfile,
    output_type=verify_refund_logic,
)

@agent.system_prompt
def add_user_contenxt(ctx: RunContext[UserProfile]):
    return f"""
    You are a refund agent.
    
    CURRENT USER DETAILS:
    - Name: {ctx.deps.name}
    - ID: {ctx.deps.id}
    - Loyalty Tier: {ctx.deps.loyalty_tier.value} <--- CRITICAL!
    
    RULES:
    1. GOLD Tier: Instant refund if item < $100. DO NOT CHECK ELIGIBILITY.
    2. SILVER Tier: Refund up to $50, but MUST check eligibility.
    3. BRONZE Tier: Manual approval (ESCALATE) if item > $20. Always check eligibility.
    """

@agent.tool
def verify_eligibility(ctx: RunContext[UserProfile], price: str) -> bool:
    """
        Verify the eligibility of the refund request.
        Do not run this tool if the user tier is gold.
        If the user tier is silver - check if the item price is less than or equal to 50$.
        If the user tier is bronze - check if the item price is greater than 20$.
    """

    if ctx.deps.loyalty_tier == LoyaltyTier.SILVER:
        if float(price) <= 50.0:
            return Decision.APPROVED
        else:
            return Decision.REJECTED
    elif ctx.deps.loyalty_tier == LoyaltyTier.BRONZE:
        if float(price) > 20.0:
            return Decision.ESCALATE
        else:
            return Decision.APPROVED
    else:
        return Decision.APPROVED

@agent.tool_plain
def get_order(order_id: str):
    """
        Get the order details from the database.
        If the order is not found, return "Order not found" and try again.
        If the order is found, return the order details.
    """

    if order_id in orders_db:
        return {"price": orders_db[order_id]["price"], "purchase_date": orders_db[order_id]["date"]}



if __name__ == "__main__":
    result = agent.run_sync(user_prompt="I want to refund my order123", deps=UserProfile(id=123, name="John Doe", loyalty_tier=LoyaltyTier.BRONZE))
    print(result.output)

    # NOTE: show the tool calls for this message to verify what the model actually did
    for msg in result.new_messages():
        if msg.parts:
            for part in msg.parts:
                if part.part_kind == "tool-call":
                    print(f"Tool called: {part.tool_name}")