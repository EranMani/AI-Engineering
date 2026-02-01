# 📘 PydanticAI vs. Vanilla OpenAI: The Complete Field Guide

**Version:** 1.0  
**Target Audience:** Senior AI Engineers building production-ready agents.  
**Goal:** Compare PydanticAI framework patterns with their manual implementations using vanilla Python and OpenAI API.

> **Philosophy**: Understanding both approaches makes you a better engineer. Use frameworks when they add value, but know how to build it yourself when needed.

---

## Table of Contents

1. [Structured Output (The Form)](#capability-1-structured-output-the-form)
2. [Dependency Injection (The Context)](#capability-2-dependency-injection-the-context)
3. [Tools & Tool Definition](#capability-3-tools--tool-definition)
4. [Self-Correction (The Retry Loop)](#capability-4-self-correction-the-retry-loop)
5. [Streaming Responses](#capability-5-streaming-responses)
6. [Message History & Conversations](#capability-6-message-history--conversations)
7. [Dynamic System Prompts](#capability-7-dynamic-system-prompts)
8. [Result Validation & Error Handling](#capability-8-result-validation--error-handling)
9. [Multi-Tool Orchestration](#capability-9-multi-tool-orchestration)
10. [Complete Production Example](#capability-10-complete-production-example)
11. [When to Use What?](#final-verdict-when-to-use-what)

---

## Capability 1: Structured Output (The Form)

**Goal:** Force the LLM to return a validated Python object (Pydantic model), not a string.

### 🟢 PydanticAI Way (The "Magic")

**Pros:** Automatic validation loop, type safety, retry on invalid output.  
**Cons:** Framework dependency, less control over retry logic.

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class MovieResult(BaseModel):
    title: str
    year: int = Field(ge=1900, le=2030, description="Release year")
    tags: list[str] = Field(description="Genres or vibe tags")

agent = Agent('openai:gpt-4o', result_type=MovieResult)

# Returns a MovieResult object automatically
result = agent.run_sync("Tell me about Inception")
print(result.data.title)  # "Inception"
print(result.data.year)    # 2010 (validated: 1900-2030)
print(result.data.tags)    # ["Sci-Fi", "Action"]
```

### ⚪ Vanilla OpenAI Way (The "Manual" Clone)

**Strategy:** Use `client.beta.chat.completions.parse()` (OpenAI SDK >= 1.40) with Pydantic models.

**Pros:** Native SDK support, very stable, no framework dependency.  
**Cons:** Manual retry loop if validation fails, no automatic error handling.

```python
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import json

client = OpenAI()

class MovieResult(BaseModel):
    title: str
    year: int = Field(ge=1900, le=2030, description="Release year")
    tags: list[str] = Field(description="Genres or vibe tags")

def get_movie_info(query: str, max_retries: int = 3) -> MovieResult:
    """Get structured movie info with retry logic."""
    messages = [
        {"role": "system", "content": "You are a movie expert."},
        {"role": "user", "content": query}
    ]
    
    for attempt in range(max_retries):
        try:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                response_format=MovieResult,  # <--- Native Pydantic support
            )
            
            # Returns parsed object directly
            movie = completion.choices[0].message.parsed
            return movie
            
        except ValidationError as e:
            if attempt == max_retries - 1:
                raise
            
            # Add validation error to messages for retry
            error_msg = f"Validation failed: {e.errors()}. Please fix the response."
            messages.append({
                "role": "assistant",
                "content": json.dumps(completion.choices[0].message.content)
            })
            messages.append({
                "role": "user",
                "content": error_msg
            })

# Usage
movie = get_movie_info("Tell me about Inception")
print(movie.title)  # "Inception"
print(movie.year)    # 2010
print(movie.tags)    # ["Sci-Fi", "Action"]
```

**Alternative: Manual JSON Parsing** (For older SDK versions or more control)

```python
from pydantic import BaseModel, ValidationError
from openai import OpenAI
import json

client = OpenAI()

class MovieResult(BaseModel):
    title: str
    year: int
    tags: list[str]

def get_movie_manual(query: str, max_retries: int = 3) -> MovieResult:
    """Manual structured output with JSON parsing."""
    messages = [
        {
            "role": "system",
            "content": "You are a movie expert. Always respond with valid JSON matching this schema: {'title': str, 'year': int, 'tags': [str]}"
        },
        {"role": "user", "content": query}
    ]
    
    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"}  # Force JSON mode
        )
        
        content = response.choices[0].message.content
        
        try:
            # Parse JSON and validate with Pydantic
            data = json.loads(content)
            return MovieResult(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == max_retries - 1:
                raise ValueError(f"Failed to parse after {max_retries} attempts: {e}")
            
            # Add error to messages for retry
            messages.append({
                "role": "assistant",
                "content": content
            })
            messages.append({
                "role": "user",
                "content": f"Invalid JSON or schema. Error: {e}. Please fix and try again."
            })

movie = get_movie_manual("Tell me about Inception")
```

---

## Capability 2: Dependency Injection (The Context)

**Goal:** Inject runtime data (User Info, DB connections) into prompts safely without string formatting hell.

### 🟢 PydanticAI Way

**Pros:** Clean separation, type-safe context, automatic validation.  
**Cons:** Requires understanding `RunContext`, framework dependency.

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class UserContext:
    username: str
    subscription_level: str  # "free" or "premium"
    user_id: str

agent = Agent('openai:gpt-4o', deps_type=UserContext)

@agent.system_prompt
def add_user_rules(ctx: RunContext[UserContext]) -> str:
    base_prompt = "You are a helpful assistant."
    
    if ctx.deps.subscription_level == "free":
        return f"{base_prompt} Keep answers short (max 2 sentences)."
    
    return f"{base_prompt} Provide detailed, comprehensive answers."

# Inject at runtime
alice = UserContext(username="Alice", subscription_level="premium", user_id="user_123")
result = agent.run_sync("Explain Quantum Physics", deps=alice)
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Use Python functions to build system prompts dynamically before API calls.

**Pros:** Zero magic, easy to debug, full control.  
**Cons:** Gets messy with many variables, no automatic validation.

```python
from dataclasses import dataclass
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

@dataclass
class UserContext:
    username: str
    subscription_level: str
    user_id: str

def build_system_prompt(user: UserContext) -> str:
    """Build dynamic system prompt based on user context."""
    base_prompt = "You are a helpful assistant."
    
    if user.subscription_level == "free":
        return f"{base_prompt} Keep answers short (max 2 sentences)."
    
    return f"{base_prompt} Provide detailed, comprehensive answers."

def chat_with_context(query: str, user: UserContext) -> str:
    """Chat with user context injected."""
    system_content = build_system_prompt(user)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": query}
        ]
    )
    
    return response.choices[0].message.content

# Usage
alice = UserContext(username="Alice", subscription_level="premium", user_id="user_123")
result = chat_with_context("Explain Quantum Physics", alice)
print(result)
```

**Advanced: Multiple Context Sources**

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class UserContext(BaseModel):
    user_id: str
    email: str
    role: str

class RequestContext(BaseModel):
    request_id: str
    timestamp: float
    ip_address: str

def pydantic_to_markdown(model: BaseModel) -> str:
    """Convert Pydantic model to markdown for better LLM parsing."""
    lines = []
    for field_name, field_value in model.model_dump().items():
        if isinstance(field_value, list):
            lines.append(f"### {field_name}")
            for item in field_value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        lines.append(f"- **{k}**: {v}")
                else:
                    lines.append(f"- {item}")
        else:
            lines.append(f"**{field_name}**: {field_value}")
    return "\n".join(lines)

def build_context_prompt(user: UserContext, request: RequestContext) -> str:
    """Build prompt with multiple context sources."""
    base = "You are a helpful assistant."
    user_md = pydantic_to_markdown(user)
    request_md = pydantic_to_markdown(request)
    
    return f"""{base}

## User Context
{user_md}

## Request Context
{request_md}
"""

def chat_with_full_context(query: str, user: UserContext, request: RequestContext) -> str:
    """Chat with multiple context sources."""
    system_content = build_context_prompt(user, request)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": query}
        ]
    )
    
    return response.choices[0].message.content
```

---

## Capability 3: Tools & Tool Definition

**Goal:** Give the agent functions to call (tools/functions).

### 🟢 PydanticAI Way

**Pros:** Auto-generates JSON schema from function signature, clean decorator syntax.  
**Cons:** Framework dependency, less control over schema generation.

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o')

@agent.tool
def get_weather(city: str, country: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}, {country}"

@agent.tool
def get_order_status(ctx: RunContext, order_id: str) -> str:
    """Check status of an order. Order IDs must start with '#'."""
    # Can access ctx.deps if deps_type is set
    return f"Order {order_id} is Shipped."

# Agent automatically knows about these tools
result = agent.run_sync("What's the weather in London?")
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Use Pydantic models to generate JSON schema manually, then pass to `tools` parameter.

**Pros:** Total control over schema, no framework dependency.  
**Cons:** More boilerplate, manual schema generation.

```python
from pydantic import BaseModel, Field
from openai import OpenAI
import json

client = OpenAI()

# 1. Define Argument Schemas (Pydantic models)
class WeatherArgs(BaseModel):
    city: str = Field(description="City name")
    country: str = Field(description="Country name")

class OrderStatusArgs(BaseModel):
    order_id: str = Field(description="Order ID, must start with '#'")

# 2. Define Functions
def get_weather(city: str, country: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}, {country}"

def get_order_status(order_id: str) -> str:
    """Check status of an order. Order IDs must start with '#'."""
    if not order_id.startswith("#"):
        return f"Error: Order ID must start with '#'. Got: {order_id}"
    return f"Order {order_id} is Shipped."

# 3. Create Tool Definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": WeatherArgs.model_json_schema()  # <--- Auto-generate JSON
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Check status of an order",
            "parameters": OrderStatusArgs.model_json_schema()
        }
    }
]

# 4. Chat with Tools
def chat_with_tools(query: str) -> str:
    """Chat with function calling enabled."""
    messages = [{"role": "user", "content": query}]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"  # Let model decide when to use tools
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        # Check if model wants to call a tool
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                # Execute tool
                if func_name == "get_weather":
                    result = get_weather(**args)
                elif func_name == "get_order_status":
                    result = get_order_status(**args)
                else:
                    result = f"Unknown function: {func_name}"
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            # Model is done, return final response
            return msg.content

# Usage
result = chat_with_tools("What's the weather in London, UK?")
print(result)
```

**Advanced: Tools with Context (Dependencies)**

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from openai import OpenAI
import json

client = OpenAI()

@dataclass
class AgentContext:
    user_id: str
    db_connection: str  # Example: database connection string

class GetInvoiceArgs(BaseModel):
    invoice_id: str = Field(description="Invoice ID format: INV-XXXX")

def get_invoice_with_context(invoice_id: str, context: AgentContext) -> str:
    """Get invoice - needs context for user_id."""
    # Use context.user_id to ensure user owns the invoice
    return f"Invoice {invoice_id} for user {context.user_id}: PAID"

def chat_with_contextual_tools(query: str, context: AgentContext) -> str:
    """Chat with tools that need context."""
    messages = [{"role": "user", "content": query}]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_invoice",
                    "description": "Get invoice details",
                    "parameters": GetInvoiceArgs.model_json_schema()
                }
            }]
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "get_invoice":
                    args = json.loads(tool_call.function.arguments)
                    # Pass context to tool
                    result = get_invoice_with_context(args['invoice_id'], context)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
        else:
            return msg.content
```

---

## Capability 4: Self-Correction (The Retry Loop)

**Goal:** If a tool fails (e.g., "User not found"), tell the LLM so it can fix the input and retry.

### 🟢 PydanticAI Way

**Pros:** Handles retry loop logic automatically, clean error messages.  
**Cons:** Hides conversation history complexity, less control.

```python
from pydantic_ai import Agent, RunContext, ModelRetry

agent = Agent('openai:gpt-4o')

@agent.tool
def get_user(ctx: RunContext, user_id: int) -> str:
    """Get user by ID. User ID must be > 0."""
    if user_id == 0:
        # PydanticAI catches this, adds to chat history, re-prompts LLM
        raise ModelRetry("User ID 0 doesn't exist. Did you mean 1?")
    
    if user_id < 0:
        raise ModelRetry(f"User ID must be positive. Got: {user_id}")
    
    return f"User {user_id} found: John Doe"

# Agent automatically retries if ModelRetry is raised
result = agent.run_sync("Get user 0")
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Write a while loop, manage messages list, detect errors in tool results, and add them back to conversation.

**Pros:** Full visibility into conversation flow, complete control.  
**Cons:** More code, easy to create infinite loops if not careful.

```python
from openai import OpenAI
import json

client = OpenAI()

def get_user(user_id: int) -> str:
    """Get user by ID."""
    if user_id == 0:
        return "ERROR: User ID 0 doesn't exist. Did you mean 1?"
    if user_id < 0:
        return f"ERROR: User ID must be positive. Got: {user_id}"
    return f"User {user_id} found: John Doe"

def chat_with_self_correction(query: str, max_retries: int = 3) -> str:
    """Chat with self-correction on tool errors."""
    messages = [{"role": "user", "content": query}]
    retry_count = 0
    
    tools = [{
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Get user by ID. User ID must be > 0.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"}
                },
                "required": ["user_id"]
            }
        }
    }]
    
    while retry_count < max_retries:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if msg.tool_calls:
            tool_error_occurred = False
            
            for tool_call in msg.tool_calls:
                args = json.loads(tool_call.function.arguments)
                result = get_user(**args)
                
                # Check if result is an error
                if result.startswith("ERROR:"):
                    tool_error_occurred = True
                    # Add error as tool result - LLM will see this and retry
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result  # Contains error message
                    })
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            
            # If error occurred, continue loop (LLM will retry)
            if tool_error_occurred:
                retry_count += 1
                continue
        else:
            # Success - return final response
            return msg.content
    
    # Max retries reached
    return "Failed to complete after maximum retries."

# Usage
result = chat_with_self_correction("Get user 0")
print(result)  # LLM will correct and ask for user 1, or handle gracefully
```

**Advanced: Structured Error Handling**

```python
from pydantic import BaseModel
from openai import OpenAI
import json
from typing import Literal

client = OpenAI()

class ToolResult(BaseModel):
    success: bool
    data: str | None = None
    error: str | None = None

def get_user_safe(user_id: int) -> ToolResult:
    """Get user with structured error handling."""
    if user_id == 0:
        return ToolResult(
            success=False,
            error="User ID 0 doesn't exist. Did you mean 1?"
        )
    if user_id < 0:
        return ToolResult(
            success=False,
            error=f"User ID must be positive. Got: {user_id}"
        )
    return ToolResult(success=True, data=f"User {user_id}: John Doe")

def chat_with_structured_errors(query: str, max_retries: int = 3) -> str:
    """Chat with structured error handling."""
    messages = [{"role": "user", "content": query}]
    retry_count = 0
    
    tools = [{
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Get user by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"}
                },
                "required": ["user_id"]
            }
        }
    }]
    
    while retry_count < max_retries:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if msg.tool_calls:
            has_error = False
            
            for tool_call in msg.tool_calls:
                args = json.loads(tool_call.function.arguments)
                result = get_user_safe(**args)
                
                # Format result as JSON for LLM
                if result.success:
                    content = json.dumps({"success": True, "data": result.data})
                else:
                    has_error = True
                    content = json.dumps({"success": False, "error": result.error})
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content
                })
            
            if has_error:
                retry_count += 1
                continue
        else:
            return msg.content
    
    return "Max retries exceeded."
```

---

## Capability 5: Streaming Responses

**Goal:** Typewriter effect - show response as it's generated, not all at once.

### 🟢 PydanticAI Way

**Pros:** Clean async context manager, handles streaming automatically.  
**Cons:** Framework dependency.

```python
import asyncio
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def stream_response():
    async with agent.run_stream("Write a long article about AI") as result:
        async for chunk in result.stream_text():
            print(chunk, end="", flush=True)  # Typewriter effect
        
        # Get final structured result if result_type is set
        final_data = await result.get_data()

asyncio.run(stream_response())
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Use `stream=True` parameter and iterate over response chunks.

**Pros:** Native SDK support, full control.  
**Cons:** Manual handling of delta content, need to reconstruct full message.

```python
from openai import OpenAI

client = OpenAI()

def stream_response(query: str):
    """Stream response with typewriter effect."""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
        stream=True  # <--- Enable streaming
    )
    
    full_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)  # Typewriter effect
            full_content += content
    
    return full_content

# Usage
result = stream_response("Write a long article about AI")
```

**Advanced: Streaming with Tools**

```python
from openai import OpenAI
import json

client = OpenAI()

def stream_with_tools(query: str):
    """Stream response even when tools are involved."""
    messages = [{"role": "user", "content": query}]
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }]
    
    while True:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            stream=True
        )
        
        full_content = ""
        tool_calls = []
        current_tool_call = None
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            
            # Handle content streaming
            if delta.content:
                print(delta.content, end="", flush=True)
                full_content += delta.content
            
            # Handle tool calls
            if delta.tool_calls:
                for tool_call_delta in delta.tool_calls:
                    if tool_call_delta.index is not None:
                        # Initialize tool call if needed
                        while len(tool_calls) <= tool_call_delta.index:
                            tool_calls.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })
                        
                        current_tool_call = tool_calls[tool_call_delta.index]
                        
                        if tool_call_delta.id:
                            current_tool_call["id"] = tool_call_delta.id
                        if tool_call_delta.function.name:
                            current_tool_call["function"]["name"] += tool_call_delta.function.name
                        if tool_call_delta.function.arguments:
                            current_tool_call["function"]["arguments"] += tool_call_delta.function.arguments
        
        # If tool calls were made, execute them
        if tool_calls:
            msg = {"role": "assistant", "content": full_content, "tool_calls": tool_calls}
            messages.append(msg)
            
            # Execute tools (simplified)
            for tool_call in tool_calls:
                if tool_call["function"]["name"] == "get_weather":
                    args = json.loads(tool_call["function"]["arguments"])
                    result = f"Sunny in {args['city']}"
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result
                    })
        else:
            # Done streaming
            messages.append({"role": "assistant", "content": full_content})
            return full_content
```

---

## Capability 6: Message History & Conversations

**Goal:** Continue conversations across multiple turns, maintaining context.

### 🟢 PydanticAI Way

**Pros:** Simple API, automatic message management.  
**Cons:** Framework dependency, less control over message format.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First turn
result1 = agent.run_sync("What is Python?")
print(result1.data)

# Continue conversation
result2 = agent.run_sync(
    "What are its main advantages?",
    message_history=result1.all_messages()  # Pass previous messages
)

# Third turn
result3 = agent.run_sync(
    "Can you give me an example?",
    message_history=result2.all_messages()  # Includes all previous
)
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Maintain a messages list, append new messages, pass entire list to each API call.

**Pros:** Full control, easy to inspect conversation.  
**Cons:** Manual management, need to track message history yourself.

```python
from openai import OpenAI

client = OpenAI()

class Conversation:
    """Manage conversation history."""
    
    def __init__(self, system_prompt: str = None):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def add_user_message(self, content: str):
        """Add user message."""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str):
        """Add assistant message."""
        self.messages.append({"role": "assistant", "content": content})
    
    def chat(self, user_message: str) -> str:
        """Send user message and get response."""
        self.add_user_message(user_message)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )
        
        assistant_message = response.choices[0].message.content
        self.add_assistant_message(assistant_message)
        
        return assistant_message
    
    def get_history(self):
        """Get full conversation history."""
        return self.messages.copy()

# Usage
conv = Conversation("You are a helpful Python tutor.")

# First turn
response1 = conv.chat("What is Python?")
print(response1)

# Second turn (automatically includes history)
response2 = conv.chat("What are its main advantages?")
print(response2)

# Third turn
response3 = conv.chat("Can you give me an example?")
print(response3)

# Access full history
print(conv.get_history())
```

**Advanced: Conversation with Tools and History**

```python
from openai import OpenAI
import json

client = OpenAI()

class ToolConversation:
    """Conversation with tool support."""
    
    def __init__(self, system_prompt: str = None):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        self.tools = []
    
    def add_tool(self, tool_def: dict):
        """Add a tool definition."""
        self.tools.append(tool_def)
    
    def chat(self, user_message: str) -> str:
        """Chat with tool support."""
        self.messages.append({"role": "user", "content": user_message})
        
        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                tools=self.tools if self.tools else None
            )
            
            msg = response.choices[0].message
            self.messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    # Execute tool (simplified)
                    result = self._execute_tool(tool_call)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                return msg.content
    
    def _execute_tool(self, tool_call):
        """Execute a tool call."""
        # Simplified - implement based on your tools
        return f"Tool {tool_call.function.name} executed"

# Usage
conv = ToolConversation("You are a helpful assistant.")
conv.add_tool({
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
})

response = conv.chat("What's the weather in London?")
```

---

## Capability 7: Dynamic System Prompts

**Goal:** Change system prompt based on runtime context (user, request, etc.).

### 🟢 PydanticAI Way

**Pros:** Clean decorator syntax, type-safe context access.  
**Cons:** Framework dependency.

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class UserContext:
    name: str
    role: str

agent = Agent('openai:gpt-4o', deps_type=UserContext)

@agent.system_prompt
def add_user_info(ctx: RunContext[UserContext]) -> str:
    return f"The user's name is {ctx.deps.name} and they are a {ctx.deps.role}."

# Multiple system prompts are combined
@agent.system_prompt
def add_rules(ctx: RunContext[UserContext]) -> str:
    if ctx.deps.role == "admin":
        return "You have admin privileges."
    return "You have standard user privileges."

result = agent.run_sync("Hello", deps=UserContext(name="Alice", role="admin"))
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Build system prompt dynamically before each API call.

**Pros:** Full control, easy to debug.  
**Cons:** Manual prompt building, no automatic combination.

```python
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI()

@dataclass
class UserContext:
    name: str
    role: str

def build_system_prompt(user: UserContext) -> str:
    """Build dynamic system prompt."""
    prompts = []
    
    # Base prompt
    prompts.append("You are a helpful assistant.")
    
    # User info
    prompts.append(f"The user's name is {user.name} and they are a {user.role}.")
    
    # Role-based rules
    if user.role == "admin":
        prompts.append("You have admin privileges.")
    else:
        prompts.append("You have standard user privileges.")
    
    return "\n".join(prompts)

def chat_with_dynamic_prompt(query: str, user: UserContext) -> str:
    """Chat with dynamically built system prompt."""
    system_content = build_system_prompt(user)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": query}
        ]
    )
    
    return response.choices[0].message.content

# Usage
user = UserContext(name="Alice", role="admin")
result = chat_with_dynamic_prompt("Hello", user)
```

**Advanced: Composable Prompt Builders**

```python
from typing import Callable, List
from openai import OpenAI

client = OpenAI()

class PromptBuilder:
    """Build system prompts from multiple sources."""
    
    def __init__(self):
        self.prompt_parts: List[str] = []
        self.builders: List[Callable] = []
    
    def add_base(self, prompt: str):
        """Add base prompt."""
        self.prompt_parts.append(prompt)
        return self
    
    def add_builder(self, builder: Callable):
        """Add a dynamic prompt builder."""
        self.builders.append(builder)
        return self
    
    def build(self, **context) -> str:
        """Build final prompt from all parts and builders."""
        parts = self.prompt_parts.copy()
        
        for builder in self.builders:
            part = builder(**context)
            if part:
                parts.append(part)
        
        return "\n".join(parts)

# Usage
def user_info_builder(**context) -> str:
    user = context.get("user")
    if user:
        return f"User: {user.name} ({user.role})"
    return ""

def role_rules_builder(**context) -> str:
    user = context.get("user")
    if user and user.role == "admin":
        return "You have admin privileges."
    return "You have standard user privileges."

builder = PromptBuilder()
builder.add_base("You are a helpful assistant.")
builder.add_builder(user_info_builder)
builder.add_builder(role_rules_builder)

system_prompt = builder.build(user=UserContext(name="Alice", role="admin"))
```

---

## Capability 8: Result Validation & Error Handling

**Goal:** Validate LLM output and handle errors gracefully.

### 🟢 PydanticAI Way

**Pros:** Automatic validation, built-in error handling, retry logic.  
**Cons:** Framework dependency, less control.

```python
from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent, UnexpectedModelBehavior

class ResponseModel(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)

agent = Agent('openai:gpt-4o', result_type=ResponseModel, retries=3)

try:
    result = agent.run_sync("Answer this question")
    print(result.data.answer)
except UnexpectedModelBehavior as e:
    print(f"Agent failed after retries: {e}")
except Exception as e:
    print(f"System error: {e}")
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Manual validation loop with retry logic and error handling.

**Pros:** Full control, can customize validation logic.  
**Cons:** More code, need to handle all edge cases.

```python
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import json

client = OpenAI()

class ResponseModel(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)

def get_validated_response(query: str, max_retries: int = 3) -> ResponseModel:
    """Get response with validation and retry."""
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Always respond with valid JSON."
        },
        {"role": "user", "content": query}
    ]
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Validate with Pydantic
            result = ResponseModel(**data)
            return result
            
        except json.JSONDecodeError as e:
            if attempt == max_retries - 1:
                raise ValueError(f"Failed to parse JSON after {max_retries} attempts: {e}")
            
            messages.append({
                "role": "assistant",
                "content": content
            })
            messages.append({
                "role": "user",
                "content": f"Invalid JSON. Error: {e}. Please fix and respond with valid JSON."
            })
            
        except ValidationError as e:
            if attempt == max_retries - 1:
                raise ValueError(f"Validation failed after {max_retries} attempts: {e}")
            
            messages.append({
                "role": "assistant",
                "content": content
            })
            messages.append({
                "role": "user",
                "content": f"Response doesn't match schema. Errors: {e.errors()}. Please fix."
            })
    
    raise RuntimeError("Max retries exceeded")

# Usage with error handling
try:
    result = get_validated_response("Answer this question")
    print(result.answer)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"System error: {e}")
```

**Advanced: Custom Validators**

```python
from pydantic import BaseModel, field_validator
from openai import OpenAI

client = OpenAI()

class BusinessResponse(BaseModel):
    answer: str
    requires_human: bool
    
    @field_validator('answer')
    @classmethod
    def validate_answer(cls, v: str) -> str:
        if len(v) < 10:
            raise ValueError("Answer must be at least 10 characters")
        if any(word in v.lower() for word in ['error', 'cannot', 'unable']):
            raise ValueError("Answer contains error indicators")
        return v

def get_business_response(query: str) -> BusinessResponse:
    """Get response with custom business validation."""
    messages = [{"role": "user", "content": query}]
    
    for attempt in range(3):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        try:
            data = json.loads(response.choices[0].message.content)
            return BusinessResponse(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            messages.append({
                "role": "user",
                "content": f"Validation failed: {e}. Please provide a better answer."
            })
    
    raise ValueError("Failed after retries")
```

---

## Capability 9: Multi-Tool Orchestration

**Goal:** Handle multiple tools, tool chaining, and complex workflows.

### 🟢 PydanticAI Way

**Pros:** Automatic tool orchestration, clean syntax.  
**Cons:** Less control over tool execution order.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

@agent.tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny"

@agent.tool
def get_restaurants(city: str) -> str:
    return f"Restaurants in {city}: Italian, Mexican"

@agent.tool
def plan_trip(city: str, weather: str, restaurants: str) -> str:
    return f"Trip plan for {city}: {weather}, {restaurants}"

# Agent automatically orchestrates tools
result = agent.run_sync("Plan a trip to Paris")
```

### ⚪ Vanilla OpenAI Way

**Strategy:** Manual tool execution loop with state management.

**Pros:** Full control over execution order, can implement custom logic.  
**Cons:** More complex, need to handle tool dependencies.

```python
from openai import OpenAI
import json
from typing import Dict, Any

client = OpenAI()

class ToolOrchestrator:
    """Orchestrate multiple tools."""
    
    def __init__(self):
        self.tools = {}
        self.tool_results = {}
    
    def register_tool(self, name: str, func: callable, schema: dict):
        """Register a tool."""
        self.tools[name] = {
            "function": func,
            "schema": schema
        }
    
    def get_tool_definitions(self) -> list:
        """Get OpenAI tool definitions."""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": schema.get("description", ""),
                    "parameters": schema.get("parameters", {})
                }
            }
            for name, tool in self.tools.items()
        ]
    
    def execute_tool(self, name: str, arguments: dict) -> str:
        """Execute a tool."""
        if name not in self.tools:
            return f"Error: Unknown tool {name}"
        
        try:
            func = self.tools[name]["function"]
            result = func(**arguments)
            self.tool_results[name] = result
            return str(result)
        except Exception as e:
            return f"Error executing {name}: {str(e)}"
    
    def chat(self, query: str, max_iterations: int = 10) -> str:
        """Chat with tool orchestration."""
        messages = [{"role": "user", "content": query}]
        iterations = 0
        
        while iterations < max_iterations:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=self.get_tool_definitions()
            )
            
            msg = response.choices[0].message
            messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    result = self.execute_tool(name, args)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                iterations += 1
            else:
                return msg.content
        
        return "Max iterations reached"

# Usage
orchestrator = ToolOrchestrator()

def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny"

def get_restaurants(city: str) -> str:
    return f"Restaurants in {city}: Italian, Mexican"

orchestrator.register_tool(
    "get_weather",
    get_weather,
    {
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
)

orchestrator.register_tool(
    "get_restaurants",
    get_restaurants,
    {
        "description": "Get restaurants for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
)

result = orchestrator.chat("Plan a trip to Paris")
```

---

## Capability 10: Complete Production Example

**Goal:** Combine all capabilities into a production-ready system.

### 🟢 PydanticAI Way

```python
import asyncio
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ModelRetry, UnexpectedModelBehavior

@dataclass
class AgentDeps:
    user_id: str
    db_connection: str

class SupportResponse(BaseModel):
    category: str
    severity: int = Field(ge=1, le=5)
    reply: str
    needs_escalation: bool

support_agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDeps,
    result_type=SupportResponse
)

@support_agent.system_prompt
def add_context(ctx: RunContext[AgentDeps]) -> str:
    return f"User ID: {ctx.deps.user_id}"

@support_agent.tool
def check_order(ctx: RunContext[AgentDeps], order_id: str) -> str:
    if not order_id.startswith("#"):
        raise ModelRetry("Order ID must start with '#'")
    return f"Order {order_id}: Shipped"

async def handle_support(query: str, deps: AgentDeps):
    try:
        result = await support_agent.run(query, deps=deps)
        return {"success": True, "data": result.data.model_dump()}
    except UnexpectedModelBehavior:
        return {"success": False, "error": "Agent failed"}
```

### ⚪ Vanilla OpenAI Way

```python
import asyncio
from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import json

client = OpenAI()

@dataclass
class AgentDeps:
    user_id: str
    db_connection: str

class SupportResponse(BaseModel):
    category: str
    severity: int = Field(ge=1, le=5)
    reply: str
    needs_escalation: bool

class SupportAgent:
    """Production-ready support agent."""
    
    def __init__(self, deps: AgentDeps):
        self.deps = deps
        self.messages = []
        self.tools = [{
            "type": "function",
            "function": {
                "name": "check_order",
                "description": "Check order status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"}
                    },
                    "required": ["order_id"]
                }
            }
        }]
    
    def _build_system_prompt(self) -> str:
        """Build dynamic system prompt."""
        return f"""You are a support agent.
User ID: {self.deps.user_id}
Always respond with valid JSON matching the SupportResponse schema."""
    
    def _check_order(self, order_id: str) -> str:
        """Check order status."""
        if not order_id.startswith("#"):
            return f"ERROR: Order ID must start with '#'. Got: {order_id}"
        return f"Order {order_id}: Shipped"
    
    async def handle_query(self, query: str, max_retries: int = 3) -> dict:
        """Handle support query."""
        self.messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": query}
        ]
        
        retry_count = 0
        
        while retry_count < max_retries:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                tools=self.tools,
                response_format={"type": "json_object"}
            )
            
            msg = response.choices[0].message
            self.messages.append(msg)
            
            # Handle tool calls
            if msg.tool_calls:
                tool_error = False
                for tool_call in msg.tool_calls:
                    if tool_call.function.name == "check_order":
                        args = json.loads(tool_call.function.arguments)
                        result = self._check_order(args["order_id"])
                        
                        if result.startswith("ERROR:"):
                            tool_error = True
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result
                        })
                
                if tool_error:
                    retry_count += 1
                    continue
            
            # Validate response
            try:
                content = msg.content
                data = json.loads(content)
                result = SupportResponse(**data)
                return {"success": True, "data": result.model_dump()}
            except (json.JSONDecodeError, ValidationError) as e:
                retry_count += 1
                if retry_count >= max_retries:
                    return {"success": False, "error": f"Validation failed: {e}"}
                
                self.messages.append({
                    "role": "user",
                    "content": f"Invalid response. Error: {e}. Please fix."
                })
        
        return {"success": False, "error": "Max retries exceeded"}

# Usage
async def main():
    deps = AgentDeps(user_id="user_123", db_connection="postgres://...")
    agent = SupportAgent(deps)
    result = await agent.handle_query("Check order #12345")
    print(result)

asyncio.run(main())
```

---

## Final Verdict: When to Use What?

| Feature | Use PydanticAI If... | Use Vanilla OpenAI If... |
|---------|---------------------|-------------------------|
| **Complexity** | You have complex flows with many tools and user contexts | You have a simple script or just one API call |
| **Type Safety** | You want strictly typed inputs/outputs everywhere | You are okay with occasional loose typing |
| **Control** | You are okay with "Magic" (decorators, DI containers) | You want "What You See Is What You Get" code |
| **Production** | You want a structured framework to enforce best practices | You need 100% stability (standard SDKs change less often) |
| **Learning** | You're learning agent patterns and want good defaults | You want to understand every detail of the implementation |
| **Team** | Your team prefers frameworks and abstractions | Your team prefers explicit, no-magic code |
| **Debugging** | You're okay debugging framework internals when needed | You want to debug your own code, not framework code |
| **Dependencies** | Adding a framework dependency is acceptable | You want minimal dependencies |

### Hybrid Approach (Best of Both Worlds)

**Strategy:** Use PydanticAI for structured I/O and dependency injection, but build your own orchestration:

```python
# Use PydanticAI for type-safe structured output
from pydantic_ai import Agent
from pydantic import BaseModel

class Result(BaseModel):
    answer: str

agent = Agent('openai:gpt-4o', result_type=Result)

# But use vanilla OpenAI for custom workflows
from openai import OpenAI

client = OpenAI()

def custom_workflow(query: str):
    # Your own orchestration logic
    step1 = client.chat.completions.create(...)
    step2 = agent.run_sync(step1.content)  # Use PydanticAI here
    step3 = client.chat.completions.create(...)
    return combine_results(step1, step2, step3)
```

### Key Takeaways

1. **PydanticAI** = Framework with good defaults, type safety, less code
2. **Vanilla OpenAI** = Full control, explicit code, more work
3. **Hybrid** = Use each where it shines
4. **Production Rule**: Understand both approaches - frameworks break, SDKs are stable

---

## Additional Resources

- **PydanticAI Docs**: https://ai.pydantic.dev/
- **OpenAI API Reference**: https://platform.openai.com/docs/api-reference
- **OpenAI Structured Outputs**: https://platform.openai.com/docs/guides/structured-outputs
- **Pydantic Documentation**: https://docs.pydantic.dev/

**Remember**: The best engineers know when to use a framework and when to build it themselves. Master both approaches.
