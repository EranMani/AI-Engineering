"""Main API router that includes all feature routers"""
from fastapi import APIRouter
from app.api.v1 import email, progress, websocket, queue

# Create main router
router = APIRouter(prefix="/api/v1")

# Include all feature routers
router.include_router(email.router)
router.include_router(progress.router)
router.include_router(websocket.router)
router.include_router(queue.router)
