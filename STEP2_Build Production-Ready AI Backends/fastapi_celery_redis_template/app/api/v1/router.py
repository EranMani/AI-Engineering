"""Main API router that includes all feature routers

This router serves as the aggregation point for all API v1 endpoints. It combines
all feature-specific routers (email, progress, websocket, queue) into a single
router that can be included in the main FastAPI application.

WHY A MAIN ROUTER?
==================

1. **Single Include Point**
   - Main app only needs: app.include_router(router)
   - Instead of including each feature router separately
   - Cleaner main.py file

2. **API Versioning**
   - All v1 endpoints grouped under /api/v1 prefix
   - Easy to add v2, v3 later by creating similar router files
   - Clear version separation

3. **Organization**
   - All feature routers registered in one place
   - Easy to see what endpoints are available
   - Simple to add/remove features

4. **Prefix Management**
   - Main router prefix: /api/v1
   - Feature router prefixes: /email, /progress, /websocket, /queue
   - Final URLs combine: /api/v1/email/send, /api/v1/progress/status/{id}, etc.

ROUTING STRUCTURE:
==================

app/main.py
    └── app.include_router(router)  ← This router
        ├── /api/v1/email/*         ← email.router (prefix="/email")
        ├── /api/v1/progress/*      ← progress.router (prefix="/progress")
        ├── /api/v1/websocket/*     ← websocket.router (prefix="/websocket")
        └── /api/v1/queue/*         ← queue.router (prefix="/queue")

Example URLs:
- POST /api/v1/email/send
- GET /api/v1/progress/status/{task_id}
- WS /api/v1/websocket/ws/{job_id}
- GET /api/v1/queue/info/{queue_name}
"""
from fastapi import APIRouter
from app.api.v1 import email, progress, websocket, queue

# Create main router with API version prefix
# This prefix is prepended to all included routers
router = APIRouter(prefix="/api/v1")

# Include all feature routers
# Each router's prefix is combined with the main router prefix
router.include_router(email.router)      # Final prefix: /api/v1/email
router.include_router(progress.router)   # Final prefix: /api/v1/progress
router.include_router(websocket.router)  # Final prefix: /api/v1/websocket
router.include_router(queue.router)      # Final prefix: /api/v1/queue
