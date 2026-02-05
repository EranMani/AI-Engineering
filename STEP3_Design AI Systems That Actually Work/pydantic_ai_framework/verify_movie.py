from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class MovieSearchOutcome(BaseModel):
    outcome: Literal["movie_found", "movie_not_found"] = Field(description="The outcome of the movie search")
    canonical_name: str = Field(description="The official name of the movie")

@dataclass
class MovieContext:
    valid_movies: list[str]

agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a helpful assistant that can help the user find a movie.",
    deps_type=MovieContext
)

@agent.tool
def verify_movie(ctx: RunContext[MovieContext], name: str):
    """
        Search for a movie by name.
        If movie is not found, return "Movie not found" and try again. If movie still not found, update the user and apologize.
        If movie is found, return "Movie found" and the movie name.
    """
    for movie in ctx.deps.valid_movies:
        if name.lower() == movie.lower():
            return f"Movie found: {movie}"
    
    return "Movie not found"

movies = MovieContext(valid_movies=["The Last of Us", "The Witcher", "The Matrix", "The Dark Knight"])

result = agent.run_sync("I want to review the movie 'the witcher'", deps=movies, output_type=MovieSearchOutcome)
print(result.output)

