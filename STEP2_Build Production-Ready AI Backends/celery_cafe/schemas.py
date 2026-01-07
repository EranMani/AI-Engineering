from pydantic import BaseModel

class OrderSchema(BaseModel):
    customer_name: str
    coffee_type: str

class OrderResponse(BaseModel):
    order_id: str
    task_id: str
    message: str
    status_url: str