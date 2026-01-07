from fastapi import APIRouter
from pydantic import BaseModel
from worker import simulate_heavy_ai_task

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
    # 1. Send the task to Celery
    # We use .delay() to send it to the background.
    # This returns IMMEDIATELY. It does not wait for the 10s sleep.
    task = simulate_heavy_ai_task.delay(event.event_id, event.data)
    
    # 2. Return the Task ID to the user
    # The user can use this ID later to check if the job is done.
    return {
        "status": "processing", 
        "task_id": task.id,
        "message": "Your request is queued. Check back later."
    }