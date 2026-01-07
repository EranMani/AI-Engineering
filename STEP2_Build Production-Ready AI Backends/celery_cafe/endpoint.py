from fastapi import APIRouter
from celery.result import AsyncResult
import uuid
from schemas import OrderSchema, OrderResponse
from worker import make_coffee, celery_app

cafe_router = APIRouter()

@cafe_router.post("/order", response_model=OrderResponse)
async def place_order(order: OrderSchema):
    """Cashier accepts the order and sends it to the kitchen. Returns immediately (non blocking)"""
    order_id = str(uuid.uuid4())

    # Send to celery using .delay()
    task = make_coffee.delay(order_id, order.coffee_type, order.customer_name)

    return OrderResponse(
        order_id=order_id,
        task_id=task.id,
        message=f"Order received for {order.customer_name}. Please wait!",
        status_url=f"/api/v1/cafe/status/{task.id}"
    )

@cafe_router.get("/status/{task_id}")
async def get_status(task_id: str):
    """Check the status of an order"""
    task_result = AsyncResult(task_id, app=celery_app)

    # Initialize response
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": None
    }

    # Handle different task states
    if task_result.status == "SUCCESS":
        # Task completed successfully
        response["result"] = task_result.result
    elif task_result.status == "FAILURE":
        # Task failed - include error details
        response["result"] = str(task_result.info) if task_result.info else "Unknown error"
        response["error"] = str(task_result.traceback) if hasattr(task_result, 'traceback') else None
    elif task_result.status in ["GRINDING", "BREWING", "POURING"]:
        # Task is in progress with custom state
        response["result"] = task_result.info
    elif task_result.ready():
        # Task is ready but status might be something else
        response["result"] = task_result.result

    return response


    