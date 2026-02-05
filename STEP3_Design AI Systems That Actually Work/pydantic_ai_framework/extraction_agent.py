from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

class MovieReview(BaseModel):
    movie_title: str = Field(description="The title of the movie")
    rating: int = Field(description="The rating of the movie from 1 to 10", ge=1, le=10)
    positive: bool = Field(description="True if the review is positive, False if the review is negative")

agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a helpful assistant that extracts information from movie reviews."
)

result = agent.run_sync("The movie 'The Last of Us' is a great movie. It has a rating of 9 out of 10 and is positive.", output_type=MovieReview)
print(result.output)