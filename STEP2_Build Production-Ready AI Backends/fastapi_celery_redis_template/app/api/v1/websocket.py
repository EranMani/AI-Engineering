"""WebSocket API endpoints for real-time updates"""
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.tasks.websocket_tasks import generate_report
from app.schemas.websocket import GenerateReportRequest, GenerateReportResponse
from app.core.redis_client import get_async_redis_client

router = APIRouter(prefix="/websocket", tags=["WebSocket"])


@router.post("/generate-report", response_model=GenerateReportResponse)
async def trigger_report_generation(request: GenerateReportRequest):
    """
    Trigger report generation and return job_id for WebSocket connection
    
    This endpoint demonstrates:
    - Creating a task that publishes to Redis
    - Returning job_id for WebSocket connection
    """
    job_id = str(uuid.uuid4())
    
    # Send task to Celery
    generate_report.delay(job_id, request.report_type, request.parameters or {})
    
    return GenerateReportResponse(
        job_id=job_id,
        status="queued",
        websocket_url=f"/api/v1/websocket/ws/{job_id}"
    )


@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time task updates
    
    This endpoint demonstrates:
    - WebSocket connection handling
    - Redis pub/sub subscription
    - Real-time message forwarding
    - Automatic connection cleanup
    
    Args:
        websocket: WebSocket connection
        job_id: Job identifier (used as Redis channel name)
    """
    # Accept WebSocket connection
    await websocket.accept()
    
    # Get async Redis client
    redis_client = await get_async_redis_client()
    
    # Create Redis pub/sub client
    pubsub = redis_client.pubsub()
    
    try:
        # Subscribe to Redis channel (channel name = job_id)
        await pubsub.subscribe(job_id)
        
        # Send initial connection message
        await websocket.send_json({
            "status": "connected",
            "job_id": job_id,
            "message": "Waiting for task completion..."
        })
        
        # Listen for messages from Redis
        while True:
            # Get message from Redis pub/sub
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0
            )
            
            if message:
                # Decode message data
                data = json.loads(message["data"])
                
                # Forward to WebSocket client
                await websocket.send_json(data)
                
                # If task completed, close connection
                if data.get("status") == "completed":
                    break
                    
    except WebSocketDisconnect:
        print(f"[WebSocket] Client disconnected: {job_id}")
    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        try:
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        except:
            pass
    finally:
        # Cleanup
        try:
            await pubsub.unsubscribe(job_id)
            await pubsub.close()
        except:
            pass
