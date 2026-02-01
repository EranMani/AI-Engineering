"""
05_block5_control_multi_level.py
================================

Purpose:
    Demonstrates "Polymorphic" output control, allowing the AI to choose between 
    completely different data structures based on the user's request.

Key Concepts:
    1. Polymorphism (The "Shape Shifter"):
       - The ability to return different object types (e.g., FlightTicket vs HotelTicket)
       - from a single API call.

    2. Union Types (`Union[A, B]`):
       - Acts as a logical `OR`. We tell the LLM: "The output must match Schema A OR Schema B."

    3. The Discriminator (`Literal`):
       - We use `service: Literal["flight"]` to tag each schema.
       - This is critical for the parser to know WHICH schema in the Union to use 
         when validating the data.

    4. The Wrapper Pattern:
       - OpenAI's `response_format` requires a single Pydantic class.
       - We wrap the `Union` inside a general `SupportResponse` class to provide 
         a stable "envelope" for the changing content.

Engineering Insight:
    This pattern decouples your data models. You can add a `CarRentalTicket` schema 
    later without breaking the existing `Flight` or `Hotel` logic.
"""


from typing import Literal, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

class FlightTicket(BaseModel):
    service: Literal["flight"] = Field(description="The type of service being booked")
    flight_number: str = Field(description="The flight number")

class HotelTicket(BaseModel):
    service: Literal["hotel"] = Field(description="The type of service being booked")
    room_number: int = Field(description="The room number")

class SupportResponse(BaseModel):
    ticket: Union[FlightTicket, HotelTicket] = Field(description="The ticket details")

ticket_text = "I need to change my booking for flight UA123 on Dec 12th."

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with customer support tickets."},
    {"role": "user", "content": ticket_text}
]

completion = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=messages,
    response_format=SupportResponse
)

result = completion.choices[0].message.parsed

if result.ticket.service == "flight":
    print(f"Flight detected: {result.ticket.flight_number}")
elif result.ticket.service == "hotel":
    print(f"Hotel detected: {result.ticket.room_number}")



