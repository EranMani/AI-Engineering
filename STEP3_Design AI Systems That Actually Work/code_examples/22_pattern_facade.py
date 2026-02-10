import asyncio
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# --- 1. Dependencies ---
class MusicControl(BaseModel):
    genre: str = Field(description="The genre of music to play")

class ManagerControl(BaseModel):
    action: str = Field(description="The action to perform")
    reasoning: str = Field(description="The reasoning for the action")

# --- 2. Workers (Sub-Agents) ---
light_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=str,
    system_prompt="You control lights. Output 'Lights ON' or 'Lights OFF'."
)

music_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=MusicControl,
)

@music_agent.system_prompt
def add_music_context(ctx: RunContext[MusicControl]):
    return f"You control music. Output 'Playing {ctx.deps.genre}' or 'Music STOP'."

# --- 3. Tools (ASYNC IS MANDATORY HERE) ---

# Note: "async def"
async def control_lights(ctx: RunContext, action: str) -> str:
    """Turns the lights on or off."""
    print(f"  [Manager] calling Light Agent with: {action}")
    # Note: "await ... .run()"
    result = await light_agent.run(f"Please turn lights {action}", deps=action)
    return result.output

async def control_music(ctx: RunContext, genre: str) -> str:
    """Plays music of a specific genre."""
    print(f"  [Manager] calling Music Agent with: {genre}")
    deps = MusicControl(genre=genre)
    result = await music_agent.run("Start music.", deps=deps)
    return result.output

# --- 4. Manager ---
manager_agent = Agent(
    'openai:gpt-4o-mini',
    # Register the ASYNC functions
    tools=[control_lights, control_music],
    system_prompt="You are a Smart Home Manager. Use your tools to fulfill the user's request.",
    output_type=ManagerControl, 
)

# --- 5. Async Execution ---
async def main():
    print("--- User Request: Party Time! ---")
    
    # The Manager is now run asynchronously
    result = await manager_agent.run("It's party time! Turn on the lights and play some Jazz.")
    
    print("\n" + "="*30)
    print(f"FINAL DECISION: {result.output.action}")
    print(f"REASONING: {result.output.reasoning}")

if __name__ == "__main__":
    asyncio.run(main())