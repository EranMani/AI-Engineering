from bz2 import decompress
from pydantic_ai import Agent, RunContext
from typing import Union
from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class UserTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"

class User(BaseModel):
    name: str = Field(description="The name of the user")
    tier: UserTier = Field(description="The tier of the user")

class AgentResponse(BaseModel):
    response: str = Field(description="The response from the agent")

def search_faq(ctx: RunContext[User], query: str) -> str:
    return f"FAQ Search for '{query}': Have you tried turning it off and on again?"

def process_refund(ctx: RunContext[User], amount: int) -> str:
    return f"Refund of ${amount} approved for user {ctx.deps.name}!"

free_agent = Agent(
    model="gpt-5-nano",
    tools=[search_faq],
    output_type=AgentResponse,
    deps_type=User
)

@free_agent.system_prompt
def add_free_prompt(ctx: RunContext[User]):
    return f"""
        You are a Basic Support bot.
        You are talking to {ctx.deps.name}.
        You can only answer questions.
        You are NOT allowed to process refunds.
        You can advise users to upgrade the service to Premium to get refunds.
        You must be polite, friendly and mention the user's name in your response.
    """


premium_agent = Agent(
    model="gpt-5-nano",
    tools=[search_faq, process_refund],
    output_type=AgentResponse,
    deps_type=User
)

@premium_agent.system_prompt
def add_premium_prompt(ctx: RunContext[User]):
    return f"""
        You are a Premium Concierge.
        You are talking to {ctx.deps.name}.
        You can handle refunds. You can also answer questions.
        You must be polite, friendly and mention the user's name in your response.
    """

def get_support_agent(user: User) -> Agent:
    if user.tier == UserTier.FREE:
        return free_agent
    elif user.tier == UserTier.PREMIUM:
        return premium_agent
    else:
        raise ValueError(f"Unknown user tier: {user.tier}")


def main():
    print("\n" + "="*30)

    eran = User(name="Eran", tier=UserTier.FREE)
    agent = get_support_agent(eran)
    result = agent.run_sync(user_prompt="I want a refund of 50$", deps=eran)
    print(result.output.response)

    print("\n" + "="*30)

    daniel = User(name="Daniel", tier=UserTier.PREMIUM)
    agent = get_support_agent(daniel)
    result = agent.run_sync(user_prompt="I want a refund of 50$", deps=daniel)
    print(result.output.response)

if __name__ == "__main__":
    main()


