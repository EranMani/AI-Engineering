from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class User:
    name: str
    age: int
    favorite_game: str

agent = Agent(
    model="gpt-5-nano",
)

@agent.system_prompt
def address_user(ctx: RunContext[User]):
    return f"The user name is {ctx.deps.name}, {ctx.deps.age} years old, and his favorite game is {ctx.deps.favorite_game}."

result1 = agent.run_sync("Hello, how are you? im currently playing a game called 'the last of us'. do you know this game?", deps=User(name="Neo", age=25, favorite_game="Rayman"))
print(result1.output)

result2 = agent.run_sync("What is my favorite game and what game im currently playing?", message_history=result1.new_messages())
print(result2.output)