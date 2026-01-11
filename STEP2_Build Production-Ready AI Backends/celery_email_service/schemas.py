from pydantic import BaseModel, Field, EmailStr


class EmailRequest(BaseModel):
    to: EmailStr = Field(description="The email of the recipient")
    subject: str = Field(description="The subject of the mail", min_length=1)
    body: str = Field(description="The content of the mail", min_length=1)

class EmailResponse(BaseModel):
    task_id: str = Field(description="The celery task ID")
    status: str = Field(description="The current state of the task")
    message: str = Field(description="The response message")

class StatusResponse(BaseModel):
    task_id: str = Field(description="The task ID")
    status: str = Field(description="The current status of the task")
    result: str | None = Field(default=None, description="The result of the task")