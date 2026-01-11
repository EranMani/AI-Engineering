from fastapi import APIRouter
from schemas import EmailRequest, EmailResponse, StatusResponse
from worker import celery_app, send_email
from celery.result import AsyncResult

email_router = APIRouter()

@email_router.post("/send_email", response_model=EmailResponse)
async def handle_send_email(email: EmailRequest):
    print("Sending email...")

    # Call the send email task, and pass the required parameters
    task = send_email.delay(email.to, email.subject, email.body)

    return EmailResponse(
        task_id=task.id,
        status="PENDING",
        message="Currently processing..."
    )

@email_router.get("/check_status/{task_id}", response_model=StatusResponse)
async def check_mail_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    # Check if the result is ready
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
                result=str(result.info)
            )
    else:
        return StatusResponse(
                task_id=task_id,
                status=result.state,
                result="Task is currently processing"
            )

