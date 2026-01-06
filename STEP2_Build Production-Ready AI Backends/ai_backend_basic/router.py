from fastapi import APIRouter
from endpoint import events_router

# This is the master router that aggregates all sub-routers
api_router = APIRouter()

# Include the events router
# prefix means all urls in events_router will start with /api/v1
# tags=["events"] helps organize the automatic documentation 
api_router.include_router(events_router, prefix="/api/v1", tags=["events"])