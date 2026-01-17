"""Email service API endpoints"""
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.tasks.email_tasks import send_email
from app.schemas.email import EmailRequest, EmailResponse, StatusResponse

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/send", response_model=EmailResponse)
async def trigger_send_email(email: EmailRequest):
    """
    Trigger email sending task
    
    This endpoint demonstrates:
    - Creating a Celery task
    - Returning immediately with task_id
    - Non-blocking task execution
    """
    # Send task to Celery queue
    task = send_email.delay(email.to, email.subject, email.body)
    
    return EmailResponse(
        task_id=task.id,
        status="PENDING",
        message="Email queued for sending"
    )


@router.get("/status/{task_id}", response_model=StatusResponse)
async def check_email_status(task_id: str):
    """
    Check the status of an email task
    
    This endpoint demonstrates:
    - Checking task status using AsyncResult
    - Retrieving task results
    - Handling different task states
    """
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        if result.successful():
            return StatusResponse(
                task_id=task_id,
                status="SUCCESS",
                result=result.get()
            )
        else:
            return StatusResponse(
                task_id=task_id,
                status="FAILURE",
                error=str(result.info)
            )
    else:
        return StatusResponse(
            task_id=task_id,
            status=result.state,
            result="Task is still processing"
        )
