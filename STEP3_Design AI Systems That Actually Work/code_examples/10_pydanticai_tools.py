from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a game master.",
)

@agent.tool
def roll_dice(ctx: RunContext, bet: int) -> str:
    # NOTE: pydantic-ai reads the function docstring and sends it to the model as a tool description.
    """Returns 'Winner' if you bet 7, else 'Loser'."""
    return "Winner" if bet == 7 else "Loser"

result = agent.run_sync("I bet 7 on the dice!")
print(result.output)