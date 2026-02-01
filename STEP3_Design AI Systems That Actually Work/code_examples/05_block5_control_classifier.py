from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SALES = "sales"

class TicketResolution(BaseModel):
    category: TicketCategory = Field(description="The category of the ticket")
    confidence: float = Field(description="The confidence score for the category")

ticket_text = "My internet is down and I can't connect to the VPN."

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with customer support tickets."},
    {"role": "user", "content": ticket_text}
]

completion = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=messages,
    response_format=TicketResolution
)

result = completion.choices[0].message.parsed

print(f"Ticket Text: '{ticket_text}'")
print(f"Ticket Category: {result.category.value.upper()}")
print(f"Confidence Score: {result.confidence:.2f}")

if result.category == TicketCategory.TECHNICAL:
    print("Action: Routing to Engineering Team...")
elif result.category == TicketCategory.BILLING:
    print("Action: Routing to Finance Team...")