from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class MovieResult(BaseModel):
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")


agent = Agent(model="gpt-5-nano", output_type=MovieResult)

result = agent.run_sync("What is the best movie of all time?")
print(result.output)