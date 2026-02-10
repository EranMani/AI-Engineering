from pydantic_ai import Agent
from pydantic import BaseModel, Field
import asyncio
from dotenv import load_dotenv

load_dotenv()

class ScoutResult(BaseModel):
    city: str = Field(description="The city to scout")
    gems: list[str] = Field(description="A list of three distinct hidden gems in the city", min_length=3, max_length=3)

class PlannerResult(BaseModel):
    itinerary: list[str] = Field(description="A list of locations in the order they should be visited in a given one day.")

class WriterResult(BaseModel):
    blog_post: str = Field(description="A blog post about the travel itinerary")

scout_agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a travel scout. List 3 distinct, hidden gems in the given city. Be concise.",
    output_type=ScoutResult
)

planner_agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a travel planner. Given a list of locations, create a logical 1-day itinerary connecting them.",
    output_type=PlannerResult
)

writer_agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a travel blogger. Given an itinerary, write a short, exciting blog post intro about this perfect day.",
    output_type=WriterResult
)

async def main():
    city = "Paris"
    result = await scout_agent.run(user_prompt=f"Explore {city} and find 3 hidden gems.")
    print(f"Im exploring {result.output.city} and found these hidden gems: {result.output.gems}")
    
    result = await planner_agent.run(user_prompt=f"Plan a 1-day itinerary for {city} based on these gems: {result.output.gems}")
    print(f"Here's your 1-day itinerary: {result.output.itinerary}")

    result = await writer_agent.run(user_prompt=f"Write a short blog post about the travel itinerary: {result.output.itinerary}")
    print(f"Here's your blog post: {result.output.blog_post}")


if __name__ == "__main__":
    asyncio.run(main())

