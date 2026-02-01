from calendar import calendar
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with scheduling events."},
    {"role": "user", "content": "Alice and Bob are going to a Science Fair on Friday."}
]

class CalendarEvent(BaseModel):
    name: str = Field(description="The name of the event")
    date: str = Field(description="The date and time of the event")
    participants: list[str] = Field(description="Full names only")


completion = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=messages,
    response_format=CalendarEvent
)

event = completion.choices[0].message.parsed
print(event)
print(event.name)
print(f"The event is on {event.date} and the participants are {event.participants}")


