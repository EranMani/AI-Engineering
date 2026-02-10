from pydantic_ai import Agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a helpful assistant that can help the user with his questions.",
    deps_type=None
)

async def main():
    async with agent.run_stream("write a poem about the future of ai engineering") as result:
        async for message in result.stream_text():
            print(message, end="", flush=True)

asyncio.run(main())