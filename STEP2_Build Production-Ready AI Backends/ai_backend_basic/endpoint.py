from fastapi import APIRouter
from pydantic import BaseModel

# Setup a specific router for this logic
# use this to group related endpoints
events_router = APIRouter()

# define the schema (the contract)
# use pydantic. Guarantees that incoming data must match this shape
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

# The logic
# The decorator @events_router.post tell fastapi: when a post request hits this url, run this function
# async allows the server to handle other incoming requests instead of freezing.
@events_router.post("/event-handler")
async def handle_event(event: EventSchema):
    """Receives an event, validates it and process it"""
    # NOTE: In real app, the ai/llm chain logic goes here
    print(f"--- Incoming Event ---")
    print(f"ID: {event.event_id}")
    print(f"Type: {event.event_type}")
    print(f"Payload: {event.data}")

    # always return a structured response
    return {
        "status": "accepted",
        "message": "Data received and validation passed",
        "processed_id": event.event_id
    }