from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI()

class Movie(BaseModel):
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")

history = [
    {"role": "system", "content": "You are a helpful assistant that can fetch a movie based on the user request."},
    {"role": "user", "content": "what do you know about the movie 'nemo'?"}
]

response = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=history,
    response_format=Movie
)

print(response.choices[0].message.parsed)