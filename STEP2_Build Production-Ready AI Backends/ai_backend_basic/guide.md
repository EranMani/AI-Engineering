# Building Production-Ready AI Backends with FastAPI

## Table of Contents
1. [Introduction](#introduction)
2. [The Core Concept: The AI Integration Layer](#the-core-concept-the-ai-integration-layer)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Building the Server from Scratch: Step-by-Step Workflow](#building-the-server-from-scratch-step-by-step-workflow)
5. [Understanding Pydantic: Why It's Your Best Friend](#understanding-pydantic-why-its-your-best-friend)
6. [Async vs Sync: When to Use Each](#async-vs-sync-when-to-use-each)
7. [Security Best Practices](#security-best-practices)
8. [Testing Your API](#testing-your-api)
9. [Production Deployment Considerations](#production-deployment-considerations)
10. [Common Patterns and Best Practices](#common-patterns-and-best-practices)

---

## Introduction

FastAPI has become the go-to framework for building AI backends because it's:
- **Fast**: Built on Starlette and Pydantic, offering near-native performance
- **Modern**: Uses Python type hints, enabling automatic validation and documentation
- **Simple**: Minimal boilerplate code, easy to learn and maintain
- **AI-Friendly**: Integrates seamlessly with Pydantic, which is also used for LLM structured outputs

This guide will walk you through building a production-ready AI backend from scratch, explaining each component in detail.

---

## The Core Concept: The AI Integration Layer

### What Is an AI Integration Layer?

Your Python scripts (checking LLMs, running PyTorch models) are currently trapped on your laptop. To make them useful to the world (or even just a frontend team), you need to wrap them in a service that can:

1. **Receive Data**: Accept JSON input (e.g., a user prompt or an image URL)
2. **Validate It**: Ensure the data matches your expected structure (crucial for fragile AI models)
3. **Process It**: Run your AI logic (the "brain")
4. **Respond**: Send back the result in a structured format

**FastAPI** handles the receiving and responding (HTTP layer), while **Pydantic** handles the validation.

### The Flow of Operations

```
┌─────────────┐
│   Client    │ (Frontend, Webhook, Another Service)
│ Application │
└──────┬──────┘
       │ HTTP POST Request
       │ (JSON Payload)
       ▼
┌─────────────────────────────────┐
│      FastAPI Application        │
│  ┌───────────────────────────┐  │
│  │   1. Receive Request      │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │   2. Validate (Pydantic)  │  │ ← Rejects invalid data early
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │   3. Process (Your Logic) │  │ ← LLM calls, PyTorch inference, etc.
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │   4. Return Response      │  │
│  └───────────────────────────┘  │
└──────┬──────────────────────────┘
       │ HTTP Response
       │ (JSON with status code)
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

---

## Setting Up Your Environment

### Prerequisites

```bash
# Install FastAPI and Uvicorn (ASGI server)
pip install fastapi uvicorn

# Optional but recommended: For testing
pip install requests httpx pytest
```

### What is Uvicorn?

**Uvicorn** is an ASGI (Asynchronous Server Gateway Interface) server that handles HTTP connections and serves your FastAPI application. Think of it as the bridge between the internet and your Python code:

- **FastAPI** = Defines your API structure (routes, endpoints, validation)
- **Uvicorn** = Handles the actual HTTP protocol and serves your app

```bash
# Running your server
uvicorn main:app --reload

# Breaking down the command:
# - main: refers to main.py file
# - app: refers to the FastAPI instance variable in main.py
# - --reload: auto-reloads on code changes (development only)
```

This starts your server on `http://localhost:8000` by default.

---

## Building the Server from Scratch: Step-by-Step Workflow

### Step 1: Create `main.py` - The Entry Point

The `main.py` file is the front door of your application. It initializes FastAPI and tells it where to find your routes.

```python
from fastapi import FastAPI
from router import api_router

# Initialize the FastAPI application
app = FastAPI(
    title="My AI Backend",
    description="Production-ready AI backend for processing events",
    version="1.0.0"
)

# Connect the master router
# This tells FastAPI to include all routes defined in api_router
app.include_router(api_router)

# Root endpoint - health check
@app.get("/")
def health_check():
    """Simple health check to verify the server is running"""
    return {"status": "running", "message": "AI Backend is online"}
```

**Why keep `main.py` minimal?**

- **Separation of Concerns**: Your startup logic stays clean and focused
- **Scalability**: As your app grows, you won't clutter the entry point
- **Testability**: Easier to test individual components

**What happens here?**

1. `FastAPI()` creates the application instance
2. `app.include_router()` tells FastAPI to look in `router.py` for more endpoints
3. The `@app.get("/")` decorator creates a GET endpoint at the root URL

**Testing Step 1:**

```bash
# Run the server
uvicorn main:app --reload

# In another terminal or browser:
curl http://localhost:8000/
# Response: {"status":"running","message":"AI Backend is online"}

# Visit http://localhost:8000/docs for automatic API documentation
```

---

### Step 2: Create `router.py` - The Traffic Controller

The router file creates a "Router" that maps URLs to specific functions. It doesn't contain heavy logic; it just routes requests.

```python
from fastapi import APIRouter
from endpoint import events_router

# This is the master router that aggregates all sub-routers
api_router = APIRouter()

# Include the events router
# prefix: All URLs in events_router will start with /api/v1
# tags: Helps organize the automatic documentation
api_router.include_router(
    events_router,
    prefix="/api/v1",
    tags=["events"]
)
```

**Understanding the Router Pattern:**

- **`APIRouter()`**: Creates a router instance that can group related endpoints
- **`prefix="/api/v1"`**: Adds a URL prefix to all endpoints in `events_router`
  - If `events_router` has an endpoint `/event-handler`, it becomes `/api/v1/event-handler`
  - This is crucial for **API versioning** (you can add `/api/v2` later without breaking `/api/v1`)
- **`tags=["events"]`**: Groups endpoints in the automatic documentation

**Benefits of this approach:**

1. **Modularity**: Each feature area (events, users, analytics) can have its own router
2. **Versioning**: Easy to maintain multiple API versions
3. **Organization**: Clean separation between routing and business logic

**Example: Multiple Routers**

```python
from fastapi import APIRouter
from endpoint import events_router, users_router, analytics_router

api_router = APIRouter()

# Version 1 endpoints
api_router.include_router(events_router, prefix="/api/v1", tags=["events"])
api_router.include_router(users_router, prefix="/api/v1", tags=["users"])

# Version 2 endpoints (new version, old ones still work)
api_router.include_router(analytics_router, prefix="/api/v2", tags=["analytics"])
```

---

### Step 3: Create `endpoint.py` - The Logic Handler

This is where the actual work happens. Here you define:
1. **Data Schemas** (using Pydantic)
2. **Endpoint Logic** (your AI processing)

```python
from fastapi import APIRouter
from pydantic import BaseModel

# Setup a specific router for this logic
# Use this to group related endpoints
events_router = APIRouter()

# Define the schema (the contract)
# Use Pydantic. Guarantees that incoming data must match this shape
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

# The logic
# The decorator @events_router.post tells FastAPI:
# "When a POST request hits this URL, run this function"
@events_router.post("/event-handler")
async def handle_event(event: EventSchema):
    """
    Receives an event, validates it, and processes it.
    
    This endpoint expects:
    - event_id: A unique identifier for the event
    - event_type: The type of event (e.g., "user_prompt", "image_upload")
    - data: A dictionary containing the event payload
    """
    # NOTE: In a real app, your AI/LLM chain logic goes here
    print(f"--- Incoming Event ---")
    print(f"ID: {event.event_id}")
    print(f"Type: {event.event_type}")
    print(f"Payload: {event.data}")
    
    # Example: You would call your AI logic here
    # result = your_ai_pipeline.process(event.data)
    
    # Always return a structured response
    return {
        "status": "accepted",
        "message": "Data received and validation passed",
        "processed_id": event.event_id
    }
```

**Breaking Down the Endpoint:**

1. **`events_router = APIRouter()`**: Creates a router for event-related endpoints
2. **`class EventSchema(BaseModel)`**: Defines the expected data structure
3. **`@events_router.post("/event-handler")`**: Decorator that:
   - Registers this function as a POST endpoint
   - The full URL becomes: `/api/v1/event-handler` (prefix + path)
4. **`async def handle_event(event: EventSchema)`**: 
   - `async` makes this an asynchronous function (more on this later)
   - `event: EventSchema` tells FastAPI to validate incoming JSON against `EventSchema`

**What happens when a request arrives?**

```
1. Request: POST /api/v1/event-handler
   Body: {"event_id": "evt_123", "event_type": "user_prompt", "data": {...}}

2. FastAPI receives the request

3. FastAPI validates the JSON against EventSchema:
   ✓ event_id is a string? ✓
   ✓ event_type is a string? ✓
   ✓ data is a dictionary? ✓
   → If all pass: Create EventSchema instance
   → If any fail: Return 422 Unprocessable Entity with error details

4. Call handle_event() with the validated EventSchema instance

5. Execute your business logic

6. Return the response (automatically serialized to JSON)
```

---

## Understanding Pydantic: Why It's Your Best Friend

### What is Pydantic?

Pydantic is a data validation library that uses Python type hints to ensure data conforms to a defined schema. FastAPI integrates Pydantic out of the box.

### Why Pydantic is Critical for AI Backends

#### 1. **Early Validation Saves Money**

In AI applications, invalid data can be costly:
- **LLM API calls**: Each invalid request wastes tokens and money
- **Model inference**: Running a PyTorch model with wrong input dimensions crashes the server
- **Processing time**: Better to reject bad data immediately

**Example: Without Pydantic**

```python
# BAD: No validation
def process_event(request_data):
    # What if request_data["event_id"] doesn't exist?
    # What if request_data["data"] is a string instead of dict?
    # What if request_data["event_type"] is missing?
    
    event_id = request_data["event_id"]  # 💥 KeyError if missing
    event_type = request_data["event_type"]  # 💥 KeyError if missing
    data = request_data["data"]  # 💥 KeyError if missing
    
    # Now we try to use it...
    result = llm_call(data["prompt"])  # 💥 TypeError if data is not dict
    # 💸 You just wasted API credits on invalid data
```

**Example: With Pydantic**

```python
# GOOD: Validation happens automatically
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

@events_router.post("/event-handler")
async def handle_event(event: EventSchema):
    # FastAPI guarantees event.event_id, event.event_type, and event.data exist
    # FastAPI guarantees event.data is a dict
    # If validation fails, FastAPI returns 422 BEFORE your function runs
    # ✅ No wasted API calls, no crashes
    
    result = llm_call(event.data["prompt"])  # Safe to assume data is dict
```

#### 2. **Automatic Documentation**

Pydantic models automatically generate OpenAPI/Swagger documentation:

```python
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

# Visit http://localhost:8000/docs and you'll see:
# - Required fields
# - Data types
# - Example values
# - All without writing any documentation code!
```

#### 3. **Type Safety and IDE Support**

```python
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

event = EventSchema(event_id="123", event_type="test", data={})

# Your IDE knows event.event_id is a string
# Autocomplete works perfectly
# Type checkers (mypy) can validate your code
```

#### 4. **Complex Validation Examples**

Pydantic can validate complex constraints:

```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional

class UserPromptSchema(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    model: str = Field(default="gpt-4", pattern="^(gpt-3.5|gpt-4|claude-2)$")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    user_email: Optional[EmailStr] = None  # Validates email format
    
    @validator('prompt')
    def prompt_must_not_contain_bad_words(cls, v):
        bad_words = ['spam', 'hack']
        if any(word in v.lower() for word in bad_words):
            raise ValueError('Prompt contains prohibited words')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "Explain quantum physics",
                "model": "gpt-4",
                "temperature": 0.7,
                "user_email": "user@example.com"
            }
        }
```

**What this does:**
- `prompt`: Must be 1-1000 characters
- `model`: Must match one of the specified models
- `temperature`: Must be between 0.0 and 2.0
- `user_email`: Optional, but if provided must be a valid email
- `prompt_must_not_contain_bad_words`: Custom validation logic

#### 5. **Structured Outputs from LLMs**

Pydantic is also used for structured outputs from LLMs:

```python
from pydantic import BaseModel

class LLMResponse(BaseModel):
    summary: str
    sentiment: str
    confidence: float

# Many LLM libraries (OpenAI, Anthropic) support Pydantic models
# They guarantee the LLM response matches your schema
```

### Expert Tip: Schema Organization

In larger production systems, move schemas to a separate `schemas.py` file:

```python
# schemas.py
from pydantic import BaseModel

class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

class EventResponse(BaseModel):
    status: str
    message: str
    processed_id: str

# endpoint.py
from schemas import EventSchema, EventResponse

@events_router.post("/event-handler", response_model=EventResponse)
async def handle_event(event: EventSchema) -> EventResponse:
    # FastAPI validates the response matches EventResponse
    return EventResponse(
        status="accepted",
        message="Data received",
        processed_id=event.event_id
    )
```

---

## Async vs Sync: When to Use Each

### Understanding Asynchronous Programming

**Synchronous (Blocking):**
```python
@events_router.post("/event-handler")
def handle_event(event: EventSchema):  # Regular function
    # Server waits for this to complete before handling next request
    result = slow_llm_call(event.data)  # Blocks for 5 seconds
    return {"result": result}
    # During those 5 seconds, the server CANNOT handle other requests
```

**Asynchronous (Non-Blocking):**
```python
@events_router.post("/event-handler")
async def handle_event(event: EventSchema):  # Async function
    # Server can handle other requests while waiting
    result = await slow_llm_call(event.data)  # Waits, but doesn't block
    return {"result": result}
    # During those 5 seconds, the server CAN handle other requests
```

### When to Use Async

**Use `async` when your endpoint:**
1. **Makes I/O-bound operations**:
   - HTTP requests (LLM API calls, database queries)
   - File operations
   - Network requests
   
   ```python
   import httpx
   
   @events_router.post("/event-handler")
   async def handle_event(event: EventSchema):
       async with httpx.AsyncClient() as client:
           # This is I/O-bound: waiting for network response
           response = await client.post(
               "https://api.openai.com/v1/chat/completions",
               json={"prompt": event.data["prompt"]}
           )
           return {"result": response.json()}
   ```

2. **Calls async libraries**:
   - `httpx.AsyncClient` (async HTTP client)
   - `asyncpg` (async PostgreSQL driver)
   - `aiofiles` (async file operations)

3. **Needs high concurrency**:
   - Multiple users hitting your API simultaneously
   - Each request takes time (e.g., 2-5 seconds for LLM responses)

**Example: Async LLM Processing**

```python
import httpx
from typing import List

@events_router.post("/batch-process")
async def batch_process_events(events: List[EventSchema]):
    """
    Process multiple events concurrently.
    With async, all API calls happen in parallel.
    """
    async with httpx.AsyncClient() as client:
        # Create tasks for all events
        tasks = [
            client.post("https://api.openai.com/...", json=event.data)
            for event in events
        ]
        
        # Execute all tasks concurrently
        responses = await asyncio.gather(*tasks)
        
        # Process all responses
        return {"processed": len(responses)}
```

### When to Use Sync

**Use regular (sync) functions when your endpoint:**
1. **Performs CPU-bound operations**:
   - Heavy computations (matrix multiplication, image processing)
   - Running local ML models (PyTorch, TensorFlow)
   
   ```python
   import torch
   
   @events_router.post("/local-inference")
   def local_inference(image_data: ImageSchema):
       # CPU-bound: Using local GPU/CPU
       # Async won't help here (runs in thread pool anyway)
       tensor = preprocess(image_data)
       result = model(tensor)  # Local PyTorch inference
       return {"result": result}
   ```

2. **Is simple and fast**:
   - Health checks
   - Simple data transformations
   - Cached responses

   ```python
   @events_router.get("/health")
   def health_check():
       # Instant response, no I/O
       return {"status": "ok"}
   ```

### Best Practices

1. **Default to async for API endpoints** (most involve I/O)
2. **Use sync for CPU-bound work** (or run it in a background task)
3. **Don't mix blocking calls in async functions**:
   
   ```python
   # BAD
   async def handle_event(event: EventSchema):
       result = requests.post(...)  # Blocking call in async function
       return result
   
   # GOOD
   async def handle_event(event: EventSchema):
       async with httpx.AsyncClient() as client:
           result = await client.post(...)  # Non-blocking
           return result
   ```

4. **For CPU-bound work in async endpoints, use background tasks**:
   
   ```python
   from fastapi import BackgroundTasks
   
   def heavy_computation(data):
       # CPU-bound work
       result = model.process(data)
       return result
   
   @events_router.post("/process")
   async def process_event(event: EventSchema, background_tasks: BackgroundTasks):
       # Queue the heavy work
       background_tasks.add_task(heavy_computation, event.data)
       
       # Return immediately
       return {"status": "processing", "event_id": event.event_id}
   ```

---

## Security Best Practices

### 1. API Key Authentication (Bearer Token)

**Always protect your API endpoints in production!**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()
events_router = APIRouter()

# Store API keys securely (use environment variables, never hardcode)
API_KEYS = {os.getenv("API_KEY", "dev-key-change-me")}

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency that validates the API key.
    FastAPI will call this automatically for any endpoint that uses it.
    """
    token = credentials.credentials
    if token not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return token

@events_router.post("/event-handler", dependencies=[Depends(verify_api_key)])
async def handle_event(event: EventSchema):
    """Protected endpoint - requires valid API key"""
    return {"status": "accepted", "message": "Authenticated request"}
```

**Client code:**

```python
import requests

headers = {
    "Authorization": "Bearer your-api-key-here",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:8000/api/v1/event-handler",
    json={"event_id": "123", "event_type": "test", "data": {}},
    headers=headers
)
```

### 2. Rate Limiting

Prevent abuse by limiting requests per user:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@events_router.post("/event-handler")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def handle_event(request: Request, event: EventSchema):
    return {"status": "accepted"}
```

### 3. Input Sanitization

Pydantic helps, but also validate content:

```python
from pydantic import BaseModel, validator

class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict
    
    @validator('event_id')
    def validate_event_id(cls, v):
        # Prevent injection attacks
        if not v.isalnum() and '_' not in v:
            raise ValueError('event_id must be alphanumeric')
        if len(v) > 100:
            raise ValueError('event_id too long')
        return v
```

### 4. CORS Configuration

Allow only trusted origins:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Only your frontend
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

---

## Testing Your API

### Using the Interactive Docs

FastAPI automatically generates interactive documentation:

1. Start your server: `uvicorn main:app --reload`
2. Visit: `http://localhost:8000/docs` (Swagger UI)
3. Visit: `http://localhost:8000/redoc` (ReDoc)

You can test endpoints directly from the browser!

### Using Python Requests

```python
# client.py
import requests

url = "http://127.0.0.1:8000/api/v1/event-handler"

payload = {
    "event_id": "evt_1055",
    "event_type": "user_prompt",
    "data": {
        "prompt": "Explain quantum physics like I'm 5",
        "model": "gpt-4",
        "temperature": 0.7
    }
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### Testing Invalid Data

```python
# This should fail validation (data is a string, not dict)
bad_payload = {
    "event_id": "evt_1055",
    "event_type": "user_prompt",
    "data": "this should be a dict"  # Wrong type!
}

response = requests.post(url, json=bad_payload, headers=headers)
print(f"Status: {response.status_code}")  # 422 Unprocessable Entity
print(f"Error: {response.json()}")
# {
#   "detail": [
#     {
#       "loc": ["body", "data"],
#       "msg": "value is not a valid dict",
#       "type": "type_error.dict"
#     }
#   ]
# }
```

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/event-handler" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "event_type": "user_prompt",
    "data": {"prompt": "Hello"}
  }'
```

---

## Production Deployment Considerations

### 1. Environment Variables

Never hardcode secrets:

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    openai_api_key: str
    database_url: str
    
    class Config:
        env_file = ".env"  # Load from .env file

settings = Settings()
```

### 2. Error Handling

```python
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

@events_router.post("/event-handler")
async def handle_event(event: EventSchema):
    try:
        # Your AI logic here
        result = process_with_llm(event.data)
        return {"status": "success", "result": result}
    except ValueError as e:
        # User error (invalid input)
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Server error (unexpected)
        logger.error(f"Processing error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### 3. Logging

```python
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@events_router.post("/event-handler")
async def handle_event(event: EventSchema, request: Request):
    logger.info(f"Received event: {event.event_id} from {request.client.host}")
    # Process...
    logger.info(f"Processed event: {event.event_id}")
    return {"status": "accepted"}
```

### 4. Running in Production

```bash
# Use a production ASGI server like Gunicorn with Uvicorn workers
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### 5. Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Common Patterns and Best Practices

### Pattern 1: Response Models

Validate your responses too:

```python
from pydantic import BaseModel

class EventResponse(BaseModel):
    status: str
    message: str
    processed_id: str
    timestamp: str

@events_router.post("/event-handler", response_model=EventResponse)
async def handle_event(event: EventSchema):
    return EventResponse(
        status="accepted",
        message="Data received",
        processed_id=event.event_id,
        timestamp=datetime.now().isoformat()
    )
```

### Pattern 2: Dependencies

Reusable logic:

```python
from fastapi import Depends

def get_current_user(api_key: str = Depends(verify_api_key)):
    # Extract user from API key
    return {"user_id": "user_123"}

@events_router.post("/event-handler")
async def handle_event(
    event: EventSchema,
    user: dict = Depends(get_current_user)
):
    # user is automatically injected
    logger.info(f"User {user['user_id']} sent event {event.event_id}")
    return {"status": "accepted"}
```

### Pattern 3: Background Tasks

Process long-running tasks asynchronously:

```python
from fastapi import BackgroundTasks

def send_notification(event_id: str):
    # Long-running task (e.g., send email, update database)
    time.sleep(5)
    logger.info(f"Notification sent for {event_id}")

@events_router.post("/event-handler")
async def handle_event(
    event: EventSchema,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification, event.event_id)
    return {"status": "accepted", "message": "Processing in background"}
```

### Pattern 4: Request/Response Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## Summary: The Complete Workflow

1. **`main.py`**: Entry point, initializes FastAPI, includes routers
2. **`router.py`**: Routes requests to appropriate endpoints, handles versioning
3. **`endpoint.py`**: Defines schemas (Pydantic) and business logic
4. **Pydantic**: Validates input/output, saves money, prevents errors
5. **Async**: Use for I/O-bound operations (API calls, databases)
6. **Sync**: Use for CPU-bound work or simple endpoints
7. **Security**: Always add authentication, rate limiting, CORS
8. **Testing**: Use `/docs` endpoint, Python requests, or cURL
9. **Production**: Environment variables, error handling, logging, proper deployment

---

## Next Steps

1. **Add authentication** to your endpoints
2. **Integrate your AI logic** into the `handle_event` function
3. **Add more endpoints** for different use cases
4. **Set up logging and monitoring**
5. **Deploy to production** (AWS, Google Cloud, Azure, etc.)

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Python Async/Await Guide](https://docs.python.org/3/library/asyncio.html)

---

**Happy building! 🚀**

