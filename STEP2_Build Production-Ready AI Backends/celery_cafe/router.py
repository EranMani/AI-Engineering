from fastapi import APIRouter
from endpoint import cafe_router

# the master router
api_router = APIRouter()

# Include the cafe router with a prefix
api_router.include_router(
    cafe_router,
    prefix= "/cafe",
    tags=["cafe"]
)