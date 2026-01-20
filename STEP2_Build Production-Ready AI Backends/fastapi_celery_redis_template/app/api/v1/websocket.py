"""WebSocket API endpoints for real-time updates

This module demonstrates real-time task completion notifications using WebSockets
and Redis pub/sub. Unlike polling (GET /status), WebSockets provide instant
updates when tasks complete, eliminating the need for repeated status checks.

Pattern: Task publishes to Redis channel → WebSocket subscribes → Client receives
updates automatically. Better UX than polling for long-running tasks.
"""
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
    Start report generation task and return WebSocket connection URL
    
    Queues a Celery task that will publish completion to Redis when done.
    Returns job_id and WebSocket URL for real-time updates.
    
    Args:
        request: Report type and optional parameters
        
    Returns:
        GenerateReportResponse with job_id and websocket_url
        
    Example:
        POST /api/v1/websocket/generate-report
        {"report_type": "monthly", "parameters": {}}
        
        Response:
        {
            "job_id": "abc-123",
            "status": "queued",
            "websocket_url": "/api/v1/websocket/ws/abc-123"
        }
        
    Next Step:
        Connect to websocket_url to receive real-time updates
    """
    # Generate unique job ID (used as Redis channel name)
    job_id = str(uuid.uuid4())
    
    # Queue task - worker will publish to Redis channel when complete
    generate_report.delay(job_id, request.report_type, request.parameters or {})
    
    return GenerateReportResponse(
        job_id=job_id,
        status="queued",
        websocket_url=f"/api/v1/websocket/ws/{job_id}"
    )


@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time task completion updates
    
    Establishes WebSocket connection and subscribes to Redis pub/sub channel.
    When Celery task completes, it publishes to Redis, which is forwarded
    to the WebSocket client automatically. No polling needed!
    
    Flow:
    1. Client connects via WebSocket
    2. Server subscribes to Redis channel (job_id)
    3. Task publishes result to Redis when complete
    4. Server forwards message to client via WebSocket
    5. Connection closes after completion
    
    Args:
        websocket: WebSocket connection object
        job_id: Job identifier (matches Redis channel name)
        
    Example Client Connection:
        const ws = new WebSocket('ws://localhost:8000/api/v1/websocket/ws/abc-123');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.status === 'completed') {
                console.log('Report ready:', data.download_url);
            }
        };
        
    Message Types:
    - {"status": "connected", ...} - Initial connection confirmation
    - {"status": "completed", "download_url": "...", ...} - Task completed
    - {"status": "error", "message": "..."} - Error occurred
    """
    # Accept WebSocket connection (required before sending/receiving)
    await websocket.accept()
    
    # Get async Redis client for pub/sub
    redis_client = await get_async_redis_client()
    
    # Create pub/sub client for subscribing to channels
    pubsub = redis_client.pubsub()
    
    try:
        # Subscribe to Redis channel (channel name = job_id)
        # Task will publish to this channel when complete
        await pubsub.subscribe(job_id)
        
        # Send connection confirmation to client
        await websocket.send_json({
            "status": "connected",
            "job_id": job_id,
            "message": "Waiting for task completion..."
        })
        
        # Listen for messages from Redis pub/sub
        while True:
            # Poll Redis for messages (non-blocking with timeout)
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,  # Skip subscription confirmation
                timeout=1.0  # Check every second
            )
            
            if message:
                # Decode JSON message from Redis
                data = json.loads(message["data"])
                
                # Forward message to WebSocket client
                await websocket.send_json(data)
                
                # Close connection after task completion
                if data.get("status") == "completed":
                    break
                    
    except WebSocketDisconnect:
        # Client closed connection - normal cleanup
        print(f"[WebSocket] Client disconnected: {job_id}")
    except Exception as e:
        # Handle errors and notify client if possible
        print(f"[WebSocket] Error: {e}")
        try:
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        except:
            pass  # Client may have already disconnected
    finally:
        # Always cleanup Redis connections
        try:
            await pubsub.unsubscribe(job_id)
            await pubsub.close()
        except:
            pass
