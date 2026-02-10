from pydantic_ai import Agent
from dotenv import load_dotenv
from enum import Enum
from pydantic import BaseModel, Field

load_dotenv()

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SALES = "sales"
    OTHER = "other"

class UserTicket(BaseModel):
    category: TicketCategory = Field(description="The category of the user's ticket issue.")

agent = Agent(
    model="gpt-5-nano",
    system_prompt="You are a help desk router. Classify the user's issue.",
    output_type=UserTicket
)

result = agent.run_sync("My internet is down and I can't connect to the VPN.")
ticket_category = result.output.category

match ticket_category:
    case TicketCategory.TECHNICAL:  
        print("Routing to technical support...")
    case TicketCategory.BILLING:
        print("Routing to finance support...")
    case TicketCategory.SALES:
        print("Routing to sales support...")
    case TicketCategory.OTHER:
        print("Routing to general support...")

