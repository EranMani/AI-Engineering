"""Email service API endpoints

This module implements an asynchronous email service using FastAPI and Celery.
It demonstrates the producer-consumer pattern where FastAPI (producer) queues
tasks and Celery workers (consumers) process them in the background.

WHY USE APIRouter?
==================

APIRouter allows us to organize endpoints into logical groups:

1. **Modular Organization**
   - Each feature (email, progress, websocket, queue) has its own router
   - Keeps code organized and maintainable
   - Easy to find and modify specific features

2. **Prefix Management**
   - All endpoints in this router automatically get `/email` prefix
   - Final URL: `/api/v1/email/send` (from main router + this router)
   - No need to repeat prefix in each endpoint

3. **Tagging for Documentation**
   - All endpoints grouped under "Email" tag in Swagger/OpenAPI docs
   - Better API documentation organization
   - Easier for developers to understand API structure

4. **Reusability**
   - Router can be included in multiple parent routers
   - Easy to version APIs (v1, v2, etc.)
   - Can be tested independently

5. **Separation of Concerns**
   - Email endpoints isolated from other features
   - Each router handles its own dependencies and logic
   - Cleaner codebase structure

Example Structure:
    app/
    ├── api/
    │   └── v1/
    │       ├── router.py      ← Main router (includes all feature routers)
    │       ├── email.py       ← This file (email router)
    │       ├── progress.py    ← Progress router
    │       └── websocket.py   ← WebSocket router

HOW IT WORKS:
=============

1. POST /send - Triggers email task (non-blocking)
   - Client sends email request
   - FastAPI validates input
   - Creates Celery task and queues it in Redis
   - Returns immediately with task_id
   - Celery worker processes task in background

2. GET /status/{task_id} - Checks task status
   - Client provides task_id from POST response
   - FastAPI queries Redis for task status
   - Returns current state (PENDING/SUCCESS/FAILURE)
   - Client can poll this endpoint to track progress

ASYNC PATTERN BENEFITS:
=======================

- Non-blocking: FastAPI responds immediately, doesn't wait for email
- Scalable: Multiple emails can be queued simultaneously
- Resilient: Tasks retry on failure (max_retries=3)
- Trackable: Client can check status anytime using task_id
- User-friendly: Fast response times, background processing
"""
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.tasks.email_tasks import send_email
from app.schemas.email import EmailRequest, EmailResponse, StatusResponse

# Create router with prefix and tags
# prefix="/email" means all endpoints will be under /api/v1/email/
# tags=["Email"] groups these endpoints in API documentation
router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/send", response_model=EmailResponse)
async def trigger_send_email(email: EmailRequest):
    """
    Trigger email sending task (non-blocking)
    
    This endpoint queues an email task for background processing and returns
    immediately with a task_id. The actual email sending happens asynchronously
    in a Celery worker.
    
    **Request Flow:**
    1. Client sends POST request with email details
    2. FastAPI validates request using EmailRequest schema
    3. Creates Celery task and queues it in Redis
    4. Returns task_id immediately (doesn't wait for email to send)
    5. Celery worker picks up task and sends email in background
    
    **Why Non-Blocking?**
    - Email sending can take 1-5 seconds (SMTP delays)
    - User shouldn't wait for this operation
    - API remains responsive for other requests
    - Multiple emails can be queued simultaneously
    
    **Example Request:**
    ```json
    POST /api/v1/email/send
    {
        "to": "user@example.com",
        "subject": "Welcome!",
        "body": "Thank you for signing up"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "task_id": "abc-123-def-456",
        "status": "PENDING",
        "message": "Email queued for sending"
    }
    ```
    
    **Next Steps:**
    - Use the returned `task_id` to check status via GET /status/{task_id}
    - Task will be processed by Celery worker in background
    - Status changes: PENDING → STARTED → SUCCESS/FAILURE
    
    Args:
        email: EmailRequest schema containing to, subject, and body
        
    Returns:
        EmailResponse with task_id, status, and message
        
    Raises:
        ValidationError: If email data doesn't match EmailRequest schema
    """
    # .delay() queues the task in Redis and returns immediately
    # This is non-blocking - FastAPI doesn't wait for task completion
    task = send_email.delay(email.to, email.subject, email.body)
    
    # Return task_id so client can track the task status
    return EmailResponse(
        task_id=task.id,  # Unique identifier for this task
        status="PENDING",  # Initial state - task is queued but not started
        message="Email queued for sending"
    )


@router.get("/status/{task_id}", response_model=StatusResponse)
async def check_email_status(task_id: str):
    """
    Check the status of an email task
    
    This endpoint allows clients to poll for task status using the task_id
    returned from the POST /send endpoint. It queries Redis (result backend)
    to get the current state of the task.
    
    **How AsyncResult Works:**
    - AsyncResult doesn't execute the task, it only checks its status
    - Connects to Redis result backend to read task metadata
    - Returns current state without blocking
    
    **Task States:**
    - PENDING: Task is queued but not started yet
    - STARTED: Task is currently being processed by worker
    - SUCCESS: Task completed successfully (result available)
    - FAILURE: Task failed (error info available)
    - RETRY: Task is being retried after failure
    
    **Polling Pattern:**
    Client should poll this endpoint periodically:
    1. Immediately after POST /send → Usually returns "PENDING"
    2. After a few seconds → May return "STARTED" or "SUCCESS"
    3. Continue polling until status is "SUCCESS" or "FAILURE"
    
    **Example Request:**
    ```
    GET /api/v1/email/status/abc-123-def-456
    ```
    
    **Example Responses:**
    
    Task still processing:
    ```json
    {
        "task_id": "abc-123-def-456",
        "status": "PENDING",
        "result": "Task is still processing"
    }
    ```
    
    Task completed successfully:
    ```json
    {
        "task_id": "abc-123-def-456",
        "status": "SUCCESS",
        "result": "Email sent successfully to user@example.com"
    }
    ```
    
    Task failed:
    ```json
    {
        "task_id": "abc-123-def-456",
        "status": "FAILURE",
        "error": "SMTP server connection failed"
    }
    ```
    
    **Why Polling?**
    - FastAPI doesn't support long-polling by default
    - Alternative: Use WebSocket for real-time updates (see websocket.py)
    - Polling interval: 1-2 seconds is reasonable
    - Stop polling when status is SUCCESS or FAILURE
    
    Args:
        task_id: Unique task identifier from POST /send response
        
    Returns:
        StatusResponse with current task status and result/error if available
        
    Note:
        This endpoint is read-only - it only checks status, doesn't modify anything
    """
    # Create AsyncResult object to check task status
    # This connects to Redis result backend to read task metadata
    result = AsyncResult(task_id, app=celery_app)
    
    # Check if task has completed (successfully or with failure)
    if result.ready():
        if result.successful():
            # Task completed successfully - return result
            return StatusResponse(
                task_id=task_id,
                status="SUCCESS",
                result=result.get()  # Get the return value from task
            )
        else:
            # Task failed - return error information
            return StatusResponse(
                task_id=task_id,
                status="FAILURE",
                error=str(result.info)  # Error details stored in result.info
            )
    else:
        # Task is still running (PENDING, STARTED, or RETRY)
        return StatusResponse(
            task_id=task_id,
            status=result.state,  # Current state (PENDING, STARTED, etc.)
            result="Task is still processing"
        )
