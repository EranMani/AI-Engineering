# PydanticAI: Production-Ready AI Agents Guide

> **Mission**: Learn how to build type-safe, reliable AI agents using PydanticAI. This guide will transform you from a junior engineer who builds fragile agents into a senior engineer who builds production-grade systems that handle edge cases gracefully.

---

## Table of Contents

1. [What is PydanticAI?](#what-is-pydanticai)
2. [Core Philosophy: White Box vs Black Box](#core-philosophy-white-box-vs-black-box)
3. [Model Selection and Configuration](#model-selection-and-configuration)
4. [The 4 Core Pillars](#the-4-core-pillars)
5. [Production Patterns and Best Practices](#production-patterns-and-best-practices)
6. [Advantages and Disadvantages](#advantages-and-disadvantages)
7. [Complete Production Template](#complete-production-template)
8. [Real-World Case Studies](#real-world-case-studies)
9. [Common Mistakes and How to Avoid Them](#common-mistakes-and-how-to-avoid-them)
10. [Senior Engineer's Safety Checklist](#senior-engineers-safety-checklist)
11. [Early Beta Considerations](#early-beta-considerations)

---

## What is PydanticAI?

### The Simple Answer

**PydanticAI** is a Python framework for building AI agents that uses **Pydantic** (the data validation library) to ensure type safety at every step of your agent pipeline.

### The Technical Answer

PydanticAI is a lightweight framework that:
- **Validates inputs** using Pydantic models (Dependencies)
- **Validates outputs** using Pydantic models (Result Types)
- **Provides tools** for agents to call functions
- **Supports streaming** for real-time user experience
- **Enables self-correction** through retry mechanisms
- **Model agnostic** - works with multiple LLM providers (OpenAI, Anthropic, etc.)
- **Type-safe dependency injection** - novel approach to passing runtime context
- **Integration with Lockfire** - monitoring and debugging capabilities (similar to LangSmith/LangFuse)

### Why It Exists

Most AI frameworks (LangChain, LlamaIndex, etc.) are "black boxes":
- You don't know what's happening inside
- Errors are hard to debug
- Type safety is an afterthought
- You're forced to use their abstractions

**PydanticAI is different**: It's a "white box" that uses standard Python patterns (`if/else`, loops, functions) instead of custom chain languages.

---

## Core Philosophy: White Box vs Black Box

### The Black Box Problem

**Traditional Frameworks (LangChain, etc.)**:
```python
# You don't know what's happening inside
chain = LLMChain(prompt=prompt, llm=llm)
result = chain.run(input_text)  # What happens here? 🤷
```

**Problems**:
- Hidden logic (hard to debug)
- Custom abstractions (hard to learn)
- Type safety is optional (runtime errors)
- Hard to customize (locked into their patterns)

### The White Box Solution

**PydanticAI**:
```python
# You see exactly what's happening
agent = Agent('openai:gpt-4o', result_type=MovieResult)
result = agent.run_sync("Tell me about Inception")
print(result.data.title)  # Type-safe, validated ✅
```

**Benefits**:
- Transparent logic (easy to debug)
- Standard Python (you already know it)
- Type safety enforced (catch errors early)
- Fully customizable (use your own patterns)

### The Key Insight

> **PydanticAI doesn't try to hide complexity. It makes complexity manageable through type safety and standard Python patterns.**

---

## Model Selection and Configuration

Before diving into the core pillars, let's understand how to select and configure models in PydanticAI.

### Two Ways to Specify Models

PydanticAI offers two ways to specify which LLM model to use:

#### Method 1: String Format (Simple)

```python
from pydantic_ai import Agent

# Simple string format: 'provider:model-name'
agent = Agent('openai:gpt-4o', system_prompt="You are helpful.")
```

**Supported formats**:
- `'openai:gpt-4o'` - OpenAI models
- `'openai:gpt-4-turbo'` - Other OpenAI models
- `'anthropic:claude-3-opus'` - Anthropic models (when supported)
- More providers being added

#### Method 2: Model Class (Explicit)

```python
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent

# Create model instance explicitly
model = OpenAIModel('gpt-4o')
agent = Agent(model, system_prompt="You are helpful.")
```

**When to use each**:
- **String format**: Quick prototyping, simple cases
- **Model class**: When you need to reuse the model, or want explicit typing

**Note**: Model parameters (like `temperature`) are not easily configurable in early versions. This is a known limitation of the beta release.

### Three Ways to Run Agents

PydanticAI provides three methods to execute agents:

```python
# 1. Async (recommended for production)
result = await agent.run("Your query", deps=deps)

# 2. Synchronous (convenient for scripts/testing)
result = agent.run_sync("Your query", deps=deps)

# 3. Streaming (for real-time user experience)
async with agent.run_stream("Your query", deps=deps) as result:
    async for chunk in result.stream_text():
        print(chunk, end="", flush=True)
```

### Understanding the Result Object

When you run an agent, you get a `RunResult` object that contains:

```python
result = agent.run_sync("Tell me about Python")

# 1. Structured data (if result_type is specified)
print(result.data)  # Your Pydantic model instance

# 2. All messages in the conversation
print(result.messages)  # List of all messages (system, user, assistant, tool calls)

# 3. Token usage and costs
print(result.usage)  # Contains input_tokens, output_tokens, total_cost

# 4. Message history (for continuing conversations)
print(result.all_messages())  # Full conversation history

# 5. Individual message access
for msg in result.messages:
    print(f"{msg.role}: {msg.content}")  # system, user, assistant, tool
```

**Result Object Structure**:
```python
class RunResult:
    data: YourResultType  # The structured output (Pydantic model)
    messages: list[Message]  # All messages in this run
    usage: UsageStats  # Token usage and costs
    all_messages() -> list[Message]  # Full conversation history
    stream_text() -> AsyncIterator[str]  # For streaming (if used)
    get_data() -> YourResultType  # Get final structured data (async)
```

**Production Tip**: Always check `result.usage` to monitor costs and token consumption. Log this data for cost analysis and optimization.

### Continuing Conversations with Message History

One powerful feature is continuing conversations by passing message history:

```python
# First interaction
result1 = agent.run_sync("What is Python?")
print(result1.data)

# Continue the conversation
result2 = agent.run_sync(
    "What was my previous question?",
    message_history=result1.all_messages()  # Pass previous messages
)
print(result2.data)  # Agent remembers the context
```

**Use Cases**:
- Multi-turn conversations
- Context-aware responses
- Building chat interfaces

**Note**: In early beta versions, there can be issues when combining message history with tools. This is being actively fixed.

#### Practical Example: Multi-Turn Conversation

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class ConversationState(BaseModel):
    topic: str
    questions_asked: int = 0

agent = Agent('openai:gpt-4o', result_type=str)

# First turn
result1 = agent.run_sync("Tell me about Python programming")
print(result1.data)
# Output: "Python is a high-level programming language..."

# Second turn - agent remembers context
result2 = agent.run_sync(
    "What are its main advantages?",
    message_history=result1.all_messages()
)
print(result2.data)
# Output: "Python's main advantages include..."

# Third turn - continue the conversation
result3 = agent.run_sync(
    "Can you give me an example?",
    message_history=result2.all_messages()  # Includes all previous messages
)
print(result3.data)
# Output: "Here's a simple example: print('Hello, World!')..."
```

**Production Pattern**: Store `result.all_messages()` in your database/session to maintain conversation context across requests.

---

## The 4 Core Pillars

These are the fundamental concepts you must understand to build production-ready agents.

### Pillar 1: Structured Output (The Form) 📋

**Goal**: Never parse a string with Regex again. Force the LLM to return valid objects.

#### The Problem Without Structured Output

```python
# ❌ BAD: Parsing strings manually
response = llm_call("Tell me about Inception")
# Response: "Inception is a 2010 sci-fi movie with tags: action, thriller"

# Now you have to parse this string 😱
title = extract_title(response)  # Regex? String splitting? Error-prone!
year = extract_year(response)    # What if format changes?
tags = extract_tags(response)    # What if LLM uses different format?
```

**Problems**:
- Format can change (LLM inconsistency)
- Parsing is error-prone
- No validation (garbage in, garbage out)
- Hard to debug (where did it break?)

#### The Solution With Structured Output

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Define the "Shape" you want back
class MovieResult(BaseModel):
    title: str
    year: int = Field(ge=1900, le=2030, description="Release year")
    tags: list[str] = Field(description="Genres or vibe tags")

# Attach it to the agent via `result_type`
agent = Agent(
    'openai:gpt-4o',
    result_type=MovieResult, 
    system_prompt="You are a movie expert."
)

# Run it
result = agent.run_sync("Tell me about Inception")

# Type-safe, validated output ✅
print(result.data.title)  # Auto-completed: "Inception"
print(result.data.year)   # Validated: 2010 (must be 1900-2030)
print(result.data.tags)   # Validated list: ["Sci-Fi", "Action"]
```

**Benefits**:
- ✅ LLM is forced to return valid structure
- ✅ Automatic validation (catches errors early)
- ✅ Type hints work (IDE autocomplete)
- ✅ Format can't change (Pydantic enforces it)

#### Production Pattern: Nested Structures

```python
from pydantic import BaseModel, Field
from typing import Optional

class Actor(BaseModel):
    name: str
    role: str

class MovieDetails(BaseModel):
    title: str
    year: int
    director: str
    actors: list[Actor] = Field(description="Main cast")
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    tags: list[str]

agent = Agent('openai:gpt-4o', result_type=MovieDetails)

result = agent.run_sync("Tell me about The Matrix")
print(result.data.actors[0].name)  # Type-safe nested access
```

---

### Pillar 2: Dependency Injection (The Backpack) 🎒

**Goal**: Safely pass runtime context (User Info, Database Connections) without messy prompt string formatting.

#### The Problem Without Dependency Injection

```python
# ❌ BAD: String formatting hell
def handle_query(user_name, subscription_level, query):
    prompt = f"""
    User: {user_name}
    Subscription: {subscription_level}
    Query: {query}
    
    If subscription is free, keep answers short.
    """
    return llm_call(prompt)

# Problems:
# - Easy to forget to include context
# - String formatting is error-prone
# - No type safety
# - Hard to test (mock what?)
```

#### The Solution With Dependency Injection

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

# The Backpack: Define what context you need
@dataclass
class UserContext:
    username: str
    subscription_level: str  # "free" or "premium"
    user_id: str

# Create agent with dependency type
agent = Agent('openai:gpt-4o', deps_type=UserContext)

# Dynamic System Prompt (Reads from Backpack)
@agent.system_prompt
def add_user_rules(ctx: RunContext[UserContext]) -> str:
    base_prompt = "You are a helpful assistant."
    
    if ctx.deps.subscription_level == "free":
        return f"{base_prompt} Keep answers short (max 2 sentences)."
    
    return f"{base_prompt} Provide detailed, comprehensive answers."

# Usage: Pass context object
alice = UserContext(
    username="Alice", 
    subscription_level="premium",
    user_id="user_123"
)

result = agent.run_sync("Explain Quantum Physics", deps=alice)
# Agent automatically has access to Alice's context
```

**Key Points**:
- The `@agent.system_prompt` decorator allows **dynamic system prompts** based on runtime context
- You can have **multiple system prompt functions** - they all get combined
- The function receives `RunContext[YourDepsType]` - type-safe access to dependencies
- System prompts are added **in addition to** the base system prompt (not replaced)

**Benefits**:
- ✅ Type-safe context (Pydantic validates it)
- ✅ Clean separation (context vs prompt)
- ✅ Easy to test (pass mock context)
- ✅ IDE autocomplete (know what's available)
- ✅ **Automatic validation** - Invalid data is caught before the agent runs

#### Validation Example: Catching Errors Early

One of the most powerful features is automatic validation of dependencies:

```python
from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent, RunContext

class CustomerDetails(BaseModel):
    customer_id: str = Field(description="Must be a string")
    name: str
    email: str

agent = Agent('openai:gpt-4o', deps_type=CustomerDetails)

# ❌ This will fail with validation error
try:
    invalid_customer = CustomerDetails(
        customer_id=12345,  # Should be string, not int!
        name="John",
        email="john@example.com"
    )
    result = agent.run_sync("Query", deps=invalid_customer)
except ValidationError as e:
    print("Validation failed:", e)
    # Your system won't run with invalid data - caught early! ✅

# ✅ This works
valid_customer = CustomerDetails(
    customer_id="12345",  # Correct type
    name="John",
    email="john@example.com"
)
result = agent.run_sync("Query", deps=valid_customer)  # Runs successfully
```

**Production Benefit**: This ensures that every time you run an agent, you're **certain** you have the right information in the right format. No more runtime errors from invalid data!

#### Production Pattern: Database Connections

```python
from dataclasses import dataclass
from typing import Optional
import asyncpg

@dataclass
class AgentDeps:
    user_id: str
    db_pool: asyncpg.Pool  # Pass database connection
    api_key: Optional[str] = None

agent = Agent('openai:gpt-4o', deps_type=AgentDeps)

@agent.tool
async def get_user_data(ctx: RunContext[AgentDeps]) -> dict:
    """Get user's data from database."""
    async with ctx.deps.db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            ctx.deps.user_id
        )
        return dict(row) if row else {}
```

#### Production Pattern: Multi-Level Context

```python
from pydantic import BaseModel

class UserContext(BaseModel):
    user_id: str
    email: str
    role: str

class RequestContext(BaseModel):
    request_id: str
    timestamp: float
    ip_address: str

class AgentDeps(BaseModel):
    user: UserContext
    request: RequestContext
    api_key: str

agent = Agent('openai:gpt-4o', deps_type=AgentDeps)

@agent.system_prompt
def add_context(ctx: RunContext[AgentDeps]) -> str:
    return f"""
    User: {ctx.deps.user.email} (Role: {ctx.deps.user.role})
    Request ID: {ctx.deps.request.request_id}
    """
```

#### Production Pattern: Converting Pydantic Models to Markdown

When injecting dependencies into system prompts, converting Pydantic models to markdown often works better than JSON:

```python
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

class CustomerDetails(BaseModel):
    customer_id: str
    name: str
    email: str
    orders: list[dict]

agent = Agent('openai:gpt-4o', deps_type=CustomerDetails)

def pydantic_to_markdown(model: BaseModel) -> str:
    """Convert Pydantic model to markdown format."""
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

@agent.system_prompt
def inject_customer_details(ctx: RunContext[CustomerDetails]) -> str:
    markdown = pydantic_to_markdown(ctx.deps)
    return f"The following customer details are available:\n\n{markdown}"
```

**Why Markdown?**: OpenAI models often parse markdown better than JSON in prompts, leading to more reliable context understanding.

---

### Pillar 3: Tools & Self-Correction (The Hands) 🛠️

**Goal**: Let the agent fetch real data AND fix its own mistakes if it hallucinates inputs.

#### Two Types of Tools

PydanticAI supports two types of tools:

1. **`@agent.tool`** - Tools that need access to agent context (dependencies)
2. **`@agent.tool_plain`** - Tools that don't need context (standalone functions)

#### Basic Tool Pattern (With Context)

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o', deps_type=CustomerDeps)

@agent.tool
def get_order_status(ctx: RunContext[CustomerDeps], order_id: str) -> str:
    """Check status of an order. Order IDs must start with '#'."""
    # Can access ctx.deps.user_id, ctx.deps.db_pool, etc.
    user_id = ctx.deps.user_id
    # Business logic here
    return f"Order {order_id} is Shipped."
```

#### Plain Tool Pattern (Without Context)

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

@agent.tool_plain
def get_weather(city: str, country: str) -> str:
    """Get weather for a city. No context needed."""
    # Standalone function - no access to agent dependencies
    return f"Weather in {city}, {country}: Sunny, 72°F"
```

**When to use each**:
- **`@agent.tool`**: When you need database connections, user context, API keys from dependencies
- **`@agent.tool_plain`**: When the tool is completely standalone (weather, calculations, etc.)

#### Two Ways to Register Tools

**Method 1: Decorator (Recommended)**

```python
@agent.tool
def my_tool(ctx: RunContext, param: str) -> str:
    return f"Result: {param}"

# Tool is automatically registered
```

**Method 2: List Registration**

```python
from pydantic_ai import Tool

def my_tool(ctx: RunContext, param: str) -> str:
    return f"Result: {param}"

# Register tools as a list
agent = Agent(
    'openai:gpt-4o',
    tools=[Tool(my_tool)]  # Explicit registration
)
```

**Production Tip**: Use decorators for clarity, but list registration is useful when you want to conditionally add tools or reuse tool definitions across multiple agents.

#### Self-Correction Pattern (The Magic)

```python
from pydantic_ai import ModelRetry

@agent.tool
def get_order_status(ctx: RunContext, order_id: str) -> str:
    """Check status of an order. Order IDs must start with '#'."""
    
    # 1. Validation Logic
    if not order_id.startswith("#"):
        # 2. Self-Correction Trigger
        # Sends error back to LLM -> LLM fixes format -> LLM calls tool again
        raise ModelRetry(
            f"Order IDs must start with a '#'. You provided: '{order_id}'. "
            f"Please ask the user for the correct order ID format."
        )
    
    # 3. Business Logic (only runs if validation passes)
    valid_orders = {"#12345": "Shipped", "#12346": "Processing"}
    
    if order_id not in valid_orders:
        raise ModelRetry(
            f"Order {order_id} not found. Please verify the order ID with the user."
        )
    
    return f"Order {order_id} status: {valid_orders[order_id]}"
```

**How Self-Correction Works**:
1. Agent calls tool with invalid input
2. Tool raises `ModelRetry` with helpful error message
3. PydanticAI sends error back to LLM
4. LLM reads error, understands the problem
5. LLM fixes the input and calls tool again
6. Process repeats until success or max retries

**Default Behavior**: PydanticAI gives the LLM **3 chances** to fix itself. After 3 failures, it raises `UnexpectedModelBehavior`.

#### Configuring Retry Behavior

You can configure retries at multiple levels:

```python
from pydantic_ai import Agent

# 1. Agent-level retries (applies to all tools and result validation)
agent = Agent(
    'openai:gpt-4o',
    retries=5  # Give LLM 5 chances instead of default 3
)

# 2. Tool-level retries (override agent-level for specific tool)
@agent.tool(retries=2)  # This tool only gets 2 retries
def sensitive_operation(ctx: RunContext, param: str) -> str:
    if not validate(param):
        raise ModelRetry("Invalid parameter")
    return process(param)

# 3. Result validator retries (for output validation)
@agent.result_validator(retries=3)
def validate_output(result: MyResult) -> MyResult:
    if not result.meets_criteria():
        raise ModelRetry("Output doesn't meet quality standards")
    return result
```

**Production Tip**: 
- Use fewer retries for expensive operations (API calls, database queries)
- Use more retries for complex reasoning tasks
- Always set a maximum to prevent infinite loops

#### Production Pattern: Database Tools with Validation

```python
from pydantic_ai import Agent, RunContext, ModelRetry
import asyncpg

@dataclass
class AgentDeps:
    db_pool: asyncpg.Pool
    user_id: str

agent = Agent('openai:gpt-4o', deps_type=AgentDeps)

@agent.tool
async def get_invoice(ctx: RunContext[AgentDeps], invoice_id: str) -> dict:
    """
    Get invoice details. Invoice ID format: INV-XXXX where XXXX is 4 digits.
    """
    import re
    
    # Validate format
    if not re.match(r'^INV-\d{4}$', invoice_id):
        raise ModelRetry(
            f"Invalid invoice ID format: '{invoice_id}'. "
            f"Expected format: INV-XXXX (e.g., INV-1234)."
        )
    
    # Check database
    async with ctx.deps.db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM invoices 
            WHERE id = $1 AND user_id = $2
            """,
            invoice_id,
            ctx.deps.user_id
        )
        
        if not row:
            raise ModelRetry(
                f"Invoice {invoice_id} not found for your account. "
                f"Please verify the invoice ID."
            )
        
        return dict(row)
```

#### Production Pattern: External API Tools

```python
import httpx
from pydantic_ai import Agent, RunContext, ModelRetry

@agent.tool
async def get_weather(ctx: RunContext, city: str, country: str) -> dict:
    """
    Get weather for a city. City and country are required.
    """
    # Validate inputs
    if not city or len(city.strip()) < 2:
        raise ModelRetry("City name must be at least 2 characters.")
    
    if not country or len(country.strip()) < 2:
        raise ModelRetry("Country name must be at least 2 characters.")
    
    # Call external API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.weather.com/v1/current",
                params={"city": city, "country": country},
                timeout=5.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ModelRetry(
                f"Weather API returned error {e.response.status_code}. "
                f"Please verify the city and country names."
            )
        except httpx.TimeoutException:
            raise ModelRetry(
                "Weather API timed out. Please try again."
            )
```

---

### Pillar 4: Streaming (User Experience) 🌊

**Goal**: Show the response immediately (Typewriter effect) instead of waiting.

#### The Problem Without Streaming

```python
# ❌ BAD: User waits 10 seconds, then sees everything at once
result = agent.run_sync("Write a long article about AI")
print(result.data)  # User sees nothing for 10 seconds, then everything
```

#### The Solution With Streaming

```python
import asyncio
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', result_type=ArticleResult)

async def stream_response():
    async with agent.run_stream("Write a long article about AI") as result:
        # Stream text chunks as they arrive
        async for chunk in result.stream_text():
            print(chunk, end="", flush=True)  # Typewriter effect
        
        # Get final structured result
        final_result = await result.get_data()
        print(f"\n\nFinal structured data: {final_result}")

asyncio.run(stream_response())
```

#### Production Pattern: WebSocket Streaming

```python
from fastapi import WebSocket
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', result_type=ResponseModel)

async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        query = await websocket.receive_text()
        
        async with agent.run_stream(query) as result:
            # Stream text chunks to client
            async for chunk in result.stream_text():
                await websocket.send_text(chunk)
            
            # Send final structured data
            final_data = await result.get_data()
            await websocket.send_json(final_data.model_dump())
            
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
```

#### Production Pattern: Progress Updates

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def stream_with_progress(query: str, progress_callback):
    async with agent.run_stream(query) as result:
        chunk_count = 0
        
        async for chunk in result.stream_text():
            chunk_count += 1
            progress_callback(f"Received {chunk_count} chunks...")
            yield chunk
        
        progress_callback("Processing complete!")
```

---

## Production Patterns and Best Practices

### Pattern 1: Error Handling and Retries

```python
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.exceptions import ModelRetry

agent = Agent('openai:gpt-4o', result_type=ResultModel)

async def run_with_error_handling(query: str, deps: AgentDeps):
    try:
        result = await agent.run(query, deps=deps)
        return {"success": True, "data": result.data}
    
    except UnexpectedModelBehavior as e:
        # LLM failed after 3 retries
        return {
            "success": False,
            "error": "Agent could not complete the task after multiple attempts.",
            "details": str(e)
        }
    
    except Exception as e:
        # Catastrophic failure (API down, network error, etc.)
        return {
            "success": False,
            "error": "System error occurred.",
            "details": str(e)
        }
```

### Pattern 2: Logging and Monitoring

```python
import logging
from pydantic_ai import Agent, RunContext

logger = logging.getLogger(__name__)

agent = Agent('openai:gpt-4o', deps_type=AgentDeps)

@agent.tool
async def get_data(ctx: RunContext[AgentDeps], item_id: str) -> dict:
    """Get item data."""
    
    # Log tool call
    logger.info(
        f"Tool called: get_data",
        extra={
            "user_id": ctx.deps.user_id,
            "item_id": item_id,
            "request_id": ctx.deps.request_id
        }
    )
    
    try:
        result = await fetch_from_db(item_id)
        logger.info(f"Tool succeeded: get_data", extra={"item_id": item_id})
        return result
    except Exception as e:
        logger.error(f"Tool failed: get_data", extra={"item_id": item_id, "error": str(e)})
        raise
```

### Pattern 3: Rate Limiting and Caching

```python
from functools import lru_cache
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', result_type=ResultModel)

# Cache common queries
@lru_cache(maxsize=100)
def get_cached_response(query_hash: str):
    # This would integrate with Redis in production
    pass

async def run_with_caching(query: str, deps: AgentDeps):
    import hashlib
    query_hash = hashlib.md5(query.encode()).hexdigest()
    
    # Check cache first
    cached = get_cached_response(query_hash)
    if cached:
        return cached
    
    # Run agent
    result = await agent.run(query, deps=deps)
    
    # Cache result
    cache_result(query_hash, result.data)
    
    return result
```

### Pattern 4: Multi-Agent Systems

```python
from pydantic_ai import Agent

# Specialized agents
classifier_agent = Agent('openai:gpt-4o', result_type=ClassificationResult)
generator_agent = Agent('openai:gpt-4o', result_type=GeneratedContent)
validator_agent = Agent('openai:gpt-4o', result_type=ValidationResult)

async def process_with_multiple_agents(query: str, deps: AgentDeps):
    # Step 1: Classify
    classification = await classifier_agent.run(query, deps=deps)
    
    # Step 2: Generate based on classification
    if classification.data.category == "support":
        result = await generator_agent.run(
            f"Generate support response for: {query}",
            deps=deps
        )
    else:
        result = await generator_agent.run(
            f"Generate general response for: {query}",
            deps=deps
        )
    
    # Step 3: Validate output
    validation = await validator_agent.run(
        f"Validate this response: {result.data.content}",
        deps=deps
    )
    
    if not validation.data.is_valid:
        # Retry generation
        return await process_with_multiple_agents(query, deps)
    
    return result
```

---

## Advantages and Disadvantages

### Advantages ✅

#### 1. Type Safety
- **Compile-time validation**: Catch errors before runtime
- **IDE support**: Autocomplete and type hints work perfectly
- **Refactoring safety**: Change a field name? IDE finds all usages

#### 2. Standard Python
- **No custom DSL**: Use `if/else`, loops, functions you already know
- **Easy to debug**: Standard Python stack traces
- **Easy to test**: Use standard Python testing tools

#### 3. Transparent Logic
- **White box**: You see exactly what's happening
- **Easy to customize**: Add your own patterns
- **Easy to extend**: Integrate with any Python library

#### 4. Production-Ready Features
- **Self-correction**: Agents fix their own mistakes
- **Streaming**: Real-time user experience
- **Error handling**: Built-in retry mechanisms
- **Validation**: Automatic input/output validation

#### 5. Lightweight
- **Small dependency**: Just Pydantic + LLM SDK
- **Fast**: No heavy abstractions
- **Flexible**: Use with any LLM provider

### Disadvantages ❌

#### 1. Less Abstraction
- **More code**: You write more boilerplate than LangChain
- **More decisions**: You decide how to structure your agent
- **Steeper learning curve**: Need to understand Pydantic first

#### 2. Early Beta Limitations ⚠️
- **API stability**: Framework is in early beta - API may change
- **Limited model parameters**: Hard to configure temperature, top_p, etc. (as of beta)
- **Message history + tools**: Some edge cases when combining message history with tools (being fixed)
- **Production readiness**: Hesitate to use in critical production systems until stable

**Senior Engineer Note**: The framework shows great promise, but treat it as experimental for now. Use it for prototypes and non-critical features, but wait for stable release before migrating core production systems.

#### 3. Newer Framework
- **Less documentation**: Fewer examples online
- **Smaller community**: Less Stack Overflow answers
- **Rapid changes**: API might change (though it's stable now)

#### 4. No Built-in Memory
- **No conversation memory**: You manage conversation history yourself
- **No vector stores**: You integrate your own RAG solution
- **No chains**: You build your own orchestration

#### 5. Requires Pydantic Knowledge
- **Learning curve**: Must understand Pydantic models
- **Validation rules**: Need to know Field constraints
- **Type system**: Python typing knowledge required

#### 6. Tool vs Solution Philosophy
- **Not a complete ecosystem**: Unlike LangChain, it's a tool, not a full solution
- **You build orchestration**: Need to build your own patterns for complex workflows
- **Integration required**: Must integrate with other tools for RAG, memory, etc.

### When to Use PydanticAI

**Use PydanticAI when**:
- ✅ You need type safety
- ✅ You want transparent, debuggable code
- ✅ You prefer standard Python patterns
- ✅ You're building production systems
- ✅ You need fine-grained control

**Don't use PydanticAI when**:
- ❌ You need built-in RAG (use LangChain + PydanticAI)
- ❌ You need complex memory management (build your own)
- ❌ You want maximum abstraction (use LangChain)
- ❌ You're prototyping quickly (PydanticAI requires more setup)
- ❌ You need production stability immediately (wait for stable release)
- ❌ You need fine-grained model parameter control (temperature, top_p, etc.) - limited in beta

### Tool vs Solution Framework Philosophy

**Important Distinction**: PydanticAI is a **tool**, not a **solution**.

**Solution Frameworks** (LangChain, LlamaIndex):
- Try to solve everything (RAG, memory, chains, agents, etc.)
- Work well within their ecosystem
- Hard to customize or combine with other tools
- Become "all or nothing" dependencies

**Tool Frameworks** (PydanticAI):
- Focus on specific problems (type safety, structured I/O)
- Easy to integrate with other tools
- You build your own orchestration
- Stay in control of your architecture

**Senior Engineer Insight**: 
> "Don't become over-dependent on any framework. Use PydanticAI for what it's good at (type-safe structured I/O), and combine it with other tools (Instructor for structured output, your own RAG solution, etc.). This keeps you flexible and avoids technical debt."

**Example Hybrid Approach**:
```python
# Use PydanticAI for agent orchestration
from pydantic_ai import Agent

# Use Instructor for structured output (if you prefer)
from instructor import patch

# Use your own RAG solution
from my_rag import retrieve_context

# Combine them - stay flexible
agent = Agent('openai:gpt-4o', result_type=MyModel)
# ... use with your own patterns
```

---

## Complete Production Template

This template combines all pillars into a robust structure. Use this for new features.

```python
import asyncio
import logging
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ModelRetry, UnexpectedModelBehavior

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. CONFIGURATION (The "Backpack") ---
@dataclass
class AgentDeps:
    user_id: str
    db_connection_str: str  # Example of passing a 'service'
    user_location: str
    request_id: str
    api_key: Optional[str] = None

# --- 2. OUTPUT SCHEMA (The "Form") ---
class TicketResolution(BaseModel):
    category: str = Field(description="Billing, Tech Support, or General")
    severity: int = Field(ge=1, le=5, description="1 is low, 5 is critical")
    reply_message: str
    suggested_actions: list[str] = Field(default_factory=list)

# --- 3. THE AGENT ---
support_agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDeps,
    result_type=TicketResolution,
    system_prompt="You are a helpful Tier 1 Support Agent."
)

# --- 4. DYNAMIC PROMPTS ---
@support_agent.system_prompt
def inject_location(ctx: RunContext[AgentDeps]) -> str:
    return f"""
    The user is located in: {ctx.deps.user_location}. 
    Adjust timezones and business hours accordingly.
    User ID: {ctx.deps.user_id}
    Request ID: {ctx.deps.request_id}
    """

# --- 5. TOOLS (With Self-Correction) ---
@support_agent.tool
def check_invoice_status(ctx: RunContext[AgentDeps], invoice_id: str) -> str:
    """Checks if an invoice is paid. Invoice ID format: INV-XXXX."""
    
    # Logging
    logger.info(
        f"Tool called: check_invoice_status",
        extra={
            "user_id": ctx.deps.user_id,
            "invoice_id": invoice_id,
            "request_id": ctx.deps.request_id
        }
    )
    
    # Guardrail: Ensure user owns the data
    # (In production, check database)
    
    # Validation: Check format
    if not invoice_id.startswith("INV-"):
        raise ModelRetry(
            f"Invoice ID '{invoice_id}' is invalid. "
            f"Invoice IDs must start with 'INV-' (e.g., INV-100)."
        )
    
    # Mock Database Lookup (replace with real DB call)
    valid_invoices = {"INV-100": "PAID", "INV-101": "PENDING"}
    
    if invoice_id not in valid_invoices:
        raise ModelRetry(
            f"Invoice {invoice_id} not found. "
            f"Please ask the user to verify the invoice ID."
        )
    
    status = valid_invoices[invoice_id]
    logger.info(f"Invoice {invoice_id} status: {status}")
    return f"Invoice {invoice_id} status: {status}"

@support_agent.tool
def get_order_tracking(ctx: RunContext[AgentDeps], order_id: str) -> str:
    """Get tracking information for an order. Order ID format: #XXXXX."""
    
    if not order_id.startswith("#"):
        raise ModelRetry(
            f"Order ID '{order_id}' is invalid. "
            f"Order IDs must start with '#' (e.g., #12345)."
        )
    
    # Mock data (replace with real DB call)
    orders = {"#12345": "Shipped - ETA: Jan 30", "#12346": "Processing"}
    
    if order_id not in orders:
        raise ModelRetry(
            f"Order {order_id} not found. Please verify with the user."
        )
    
    return f"Order {order_id}: {orders[order_id]}"

# --- 6. EXECUTION WITH ERROR HANDLING ---
async def handle_support_query(query: str, deps: AgentDeps) -> dict:
    """
    Main entry point for support queries.
    Returns a dict with success status and data/error.
    """
    try:
        logger.info(f"Processing query: {query[:100]}...", extra={"request_id": deps.request_id})
        
        result = await support_agent.run(query, deps=deps)
        
        logger.info("Query processed successfully", extra={"request_id": deps.request_id})
        
        return {
            "success": True,
            "data": result.data.model_dump(),
            "usage": result.usage.model_dump() if hasattr(result, 'usage') else None
        }
    
    except UnexpectedModelBehavior as e:
        # LLM failed after retries
        logger.error(
            f"Agent failed after retries: {str(e)}",
            extra={"request_id": deps.request_id}
        )
        return {
            "success": False,
            "error": "I couldn't process your request. Please try rephrasing or contact human support.",
            "error_type": "model_retry_exhausted"
        }
    
    except Exception as e:
        # Catastrophic failure
        logger.exception(
            f"Unexpected error: {str(e)}",
            extra={"request_id": deps.request_id}
        )
        return {
            "success": False,
            "error": "A system error occurred. Please try again later.",
            "error_type": "system_error"
        }

# --- 7. STREAMING VERSION ---
async def handle_support_query_stream(query: str, deps: AgentDeps):
    """
    Streaming version for real-time user experience.
    """
    try:
        async with support_agent.run_stream(query, deps=deps) as result:
            # Stream text chunks
            async for chunk in result.stream_text():
                yield {"type": "chunk", "content": chunk}
            
            # Send final structured data
            final_data = await result.get_data()
            yield {
                "type": "final",
                "data": final_data.model_dump()
            }
    
    except Exception as e:
        yield {
            "type": "error",
            "error": str(e)
        }

# --- 8. MAIN EXECUTION ---
async def main():
    # Setup Context
    context = AgentDeps(
        user_id="user_123",
        db_connection_str="postgres://localhost/db",
        user_location="London, UK",
        request_id="req_456"
    )

    query = "My invoice INV-100 is showing as unpaid, can you help?"

    print(f"User Query: {query}\n" + "-" * 50)

    # Run (non-streaming)
    result = await handle_support_query(query, context)
    
    if result["success"]:
        data = result["data"]
        print(f"Category: {data['category']}")
        print(f"Severity: {data['severity']}")
        print(f"Reply: {data['reply_message']}")
        if data['suggested_actions']:
            print(f"Suggested Actions: {', '.join(data['suggested_actions'])}")
    else:
        print(f"Error: {result['error']}")

    # Run (streaming)
    print("\n" + "-" * 50)
    print("Streaming version:")
    async for chunk in handle_support_query_stream(query, context):
        if chunk["type"] == "chunk":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "final":
            print(f"\n\nFinal data: {chunk['data']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Real-World Case Studies

### Case Study 1: Customer Support Agent

#### The Problem

An e-commerce company receives 5,000 support tickets per day. They need an AI agent that can:
- Understand customer queries
- Check order/invoice status
- Generate personalized responses
- Handle errors gracefully

#### The Solution with PydanticAI

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ModelRetry
from dataclasses import dataclass

# Dependencies
@dataclass
class SupportDeps:
    user_id: str
    db_pool: asyncpg.Pool
    customer_tier: str  # "free", "premium", "enterprise"

# Output Schema
class SupportResponse(BaseModel):
    category: str = Field(description="Type of support needed")
    confidence: float = Field(ge=0.0, le=1.0)
    response: str
    requires_human: bool = Field(description="True if human escalation needed")
    suggested_actions: list[str]

# Agent
support_agent = Agent(
    'openai:gpt-4o',
    deps_type=SupportDeps,
    result_type=SupportResponse
)

# Tools
@support_agent.tool
async def check_order(ctx: RunContext[SupportDeps], order_id: str) -> str:
    """Check order status. Format: #XXXXX"""
    if not order_id.startswith("#"):
        raise ModelRetry("Order IDs must start with '#'")
    
    async with ctx.deps.db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT status FROM orders WHERE id = $1 AND user_id = $2",
            order_id, ctx.deps.user_id
        )
        if not row:
            raise ModelRetry(f"Order {order_id} not found")
        return f"Order {order_id}: {row['status']}"
```

**Why This Works**:
- ✅ Type-safe responses (no parsing errors)
- ✅ Self-correction (handles invalid order IDs)
- ✅ Database integration (real data, not hallucinations)
- ✅ Error handling (graceful failures)

### Case Study 2: Document Analysis Agent

#### The Problem

A legal firm needs to analyze contracts and extract:
- Key dates
- Parties involved
- Financial terms
- Risk factors

#### The Solution with PydanticAI

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ContractAnalysis(BaseModel):
    parties: list[str] = Field(description="Names of all parties")
    effective_date: Optional[date] = None
    expiration_date: Optional[date] = None
    total_value: Optional[float] = Field(None, ge=0)
    risk_level: str = Field(description="low, medium, or high")
    key_terms: list[str]
    requires_review: bool

analysis_agent = Agent(
    'openai:gpt-4o',
    result_type=ContractAnalysis,
    system_prompt="You are a legal contract analyst."
)

# Usage
result = await analysis_agent.run_sync(document_text)
print(f"Parties: {result.data.parties}")
print(f"Risk Level: {result.data.risk_level}")
if result.data.requires_review:
    print("⚠️ This contract requires human review")
```

**Why This Works**:
- ✅ Structured extraction (no manual parsing)
- ✅ Date validation (Pydantic ensures valid dates)
- ✅ Type safety (IDE autocomplete works)
- ✅ Production-ready (handles missing fields)

### Case Study 3: Code Review Agent

#### The Problem

A development team wants an AI agent that:
- Reviews code for bugs
- Checks style compliance
- Suggests improvements
- Returns structured feedback

#### The Solution with PydanticAI

```python
from pydantic import BaseModel, Field
from typing import Literal

class CodeIssue(BaseModel):
    line_number: int
    severity: Literal["error", "warning", "info"]
    message: str
    suggestion: Optional[str] = None

class CodeReview(BaseModel):
    overall_score: float = Field(ge=0.0, le=10.0)
    issues: list[CodeIssue]
    strengths: list[str]
    improvements: list[str]
    approved: bool

review_agent = Agent(
    'openai:gpt-4o',
    result_type=CodeReview,
    system_prompt="You are a senior code reviewer."
)

# Usage
result = await review_agent.run_sync(f"Review this code:\n{code}")
if result.data.approved:
    print("✅ Code approved")
else:
    print(f"❌ {len(result.data.issues)} issues found")
    for issue in result.data.issues:
        print(f"  Line {issue.line_number}: {issue.message}")
```

**Why This Works**:
- ✅ Structured feedback (easy to integrate into CI/CD)
- ✅ Type-safe issues (no parsing errors)
- ✅ Validation (score is always 0-10)
- ✅ Production-ready (handles edge cases)

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Forgetting to Define `result_type`

**Symptom**: Getting plain strings back, having to parse manually.

```python
# ❌ BAD
agent = Agent('openai:gpt-4o')
result = agent.run_sync("Tell me about Python")
# result.data is a string - you have to parse it 😱
```

**Fix**: Always define `result_type`.

```python
# ✅ GOOD
class PythonInfo(BaseModel):
    language: str
    year_created: int
    features: list[str]

agent = Agent('openai:gpt-4o', result_type=PythonInfo)
result = agent.run_sync("Tell me about Python")
# result.data is a PythonInfo object - type-safe! ✅
```

### Mistake 2: Not Passing Dependencies

**Symptom**: `ctx.deps` is `None`, causing AttributeError.

```python
# ❌ BAD
agent = Agent('openai:gpt-4o', deps_type=UserContext)

@agent.tool
def get_data(ctx: RunContext[UserContext]) -> str:
    return ctx.deps.user_id  # ❌ ctx.deps is None!

result = agent.run_sync("Get my data")  # Forgot deps=...
```

**Fix**: Always pass dependencies.

```python
# ✅ GOOD
context = UserContext(user_id="user_123")
result = agent.run_sync("Get my data", deps=context)  # ✅ deps passed
```

### Mistake 3: Not Handling `UnexpectedModelBehavior`

**Symptom**: App crashes when LLM fails after retries.

```python
# ❌ BAD
result = await agent.run(query)  # Crashes if LLM fails 3 times
print(result.data)
```

**Fix**: Always wrap in try/except.

```python
# ✅ GOOD
try:
    result = await agent.run(query, deps=deps)
    return result.data
except UnexpectedModelBehavior as e:
    logger.error(f"Agent failed: {e}")
    return {"error": "Could not process request"}
```

### Mistake 4: Using `ModelRetry` for Non-Retryable Errors

**Symptom**: Infinite retry loops for errors that can't be fixed.

```python
# ❌ BAD
@agent.tool
def get_data(ctx: RunContext, item_id: str) -> dict:
    if item_id not in database:
        raise ModelRetry("Item not found")  # ❌ LLM can't fix this!
    # This will retry forever...
```

**Fix**: Use `ModelRetry` only for fixable errors. Raise regular exceptions for unfixable errors.

```python
# ✅ GOOD
@agent.tool
def get_data(ctx: RunContext, item_id: str) -> dict:
    # Format error - LLM can fix this
    if not item_id.startswith("ITEM-"):
        raise ModelRetry("Item ID must start with 'ITEM-'")
    
    # Not found - LLM can't fix this, don't retry
    if item_id not in database:
        raise ValueError(f"Item {item_id} not found. Please verify the ID.")
```

### Mistake 5: Not Validating Tool Inputs

**Symptom**: Tools receive invalid data, causing crashes.

```python
# ❌ BAD
@agent.tool
def process_order(ctx: RunContext, order_id: str) -> str:
    # No validation - crashes if order_id is None or empty
    return database.get_order(order_id)
```

**Fix**: Always validate inputs in tools.

```python
# ✅ GOOD
@agent.tool
def process_order(ctx: RunContext, order_id: str) -> str:
    if not order_id or not order_id.strip():
        raise ModelRetry("Order ID cannot be empty")
    
    if not order_id.startswith("#"):
        raise ModelRetry("Order ID must start with '#'")
    
    return database.get_order(order_id)
```

### Mistake 6: Not Using Type Hints

**Symptom**: No IDE autocomplete, runtime type errors.

```python
# ❌ BAD
@agent.tool
def get_data(ctx, item_id):  # No type hints
    return ctx.deps.user_id  # IDE doesn't know what ctx.deps is
```

**Fix**: Always use type hints.

```python
# ✅ GOOD
@agent.tool
def get_data(ctx: RunContext[AgentDeps], item_id: str) -> dict:
    # IDE knows ctx.deps is AgentDeps - autocomplete works!
    return {"user_id": ctx.deps.user_id}
```

---

## Senior Engineer's Safety Checklist

Before you push to production, check these items:

### ✅ Checklist Item 1: Result Type is Defined

**Question**: Is the agent returning structured data?

**Bad**: Returning plain text strings for internal logic.
```python
agent = Agent('openai:gpt-4o')  # ❌ No result_type
```

**Good**: Always use `result_type` when the agent talks to your code.
```python
agent = Agent('openai:gpt-4o', result_type=MyModel)  # ✅
```

### ✅ Checklist Item 2: Dependencies are Passed

**Question**: Is context being passed correctly?

**Bad**: `agent.run(query)` (This passes `None` to the backpack).
```python
result = agent.run_sync(query)  # ❌ No deps
```

**Good**: Always pass dependencies.
```python
result = agent.run_sync(query, deps=my_context_object)  # ✅
```

### ✅ Checklist Item 3: Retries are Handled

**Question**: What happens when the LLM fails after 3 retries?

**Bad**: No error handling - app crashes.
```python
result = await agent.run(query)  # ❌ Crashes on failure
```

**Good**: Catch `UnexpectedModelBehavior` and handle gracefully.
```python
try:
    result = await agent.run(query, deps=deps)
except UnexpectedModelBehavior:
    return {"error": "Could not process"}  # ✅ Graceful failure
```

### ✅ Checklist Item 4: Tool Inputs are Validated

**Question**: Do tools validate their inputs?

**Bad**: Tools assume inputs are valid.
```python
@agent.tool
def get_order(order_id: str) -> str:
    return database.get(order_id)  # ❌ No validation
```

**Good**: Tools validate and use `ModelRetry` for fixable errors.
```python
@agent.tool
def get_order(order_id: str) -> str:
    if not order_id.startswith("#"):
        raise ModelRetry("Order ID must start with '#'")  # ✅ Validation
    return database.get(order_id)
```

### ✅ Checklist Item 5: Logging is Implemented

**Question**: Can you debug production issues?

**Bad**: No logging - can't debug failures.
```python
result = await agent.run(query)  # ❌ No logs
```

**Good**: Log important events.
```python
logger.info(f"Processing query: {query[:100]}")
result = await agent.run(query, deps=deps)
logger.info(f"Query processed: {result.data}")  # ✅ Logged
```

### ✅ Checklist Item 6: Streaming is Used (When Needed)

**Question**: Do users wait for the entire response?

**Bad**: Users wait 10 seconds, then see everything.
```python
result = await agent.run(query)  # ❌ No streaming
```

**Good**: Stream responses for better UX.
```python
async with agent.run_stream(query) as result:
    async for chunk in result.stream_text():
        yield chunk  # ✅ Real-time updates
```

### ✅ Checklist Item 7: Error Messages are User-Friendly

**Question**: What do users see when something fails?

**Bad**: Technical error messages.
```python
except Exception as e:
    return {"error": str(e)}  # ❌ "UnexpectedModelBehavior: ..."
```

**Good**: User-friendly error messages.
```python
except UnexpectedModelBehavior:
    return {"error": "I couldn't process your request. Please try again."}  # ✅
```

---

## Summary: Key Takeaways

### For Junior Engineers

1. **Always use `result_type`**: Never parse strings manually
2. **Always pass `deps`**: Context is essential for production systems
3. **Always handle errors**: Catch `UnexpectedModelBehavior` and other exceptions
4. **Always validate tool inputs**: Use `ModelRetry` for fixable errors
5. **Always use type hints**: They catch errors early and enable IDE support
6. **Always log important events**: You'll need to debug production issues
7. **Use streaming for UX**: Real-time updates are better than waiting

### The Golden Rules

1. **Type Safety First**: Use Pydantic models for everything
2. **Standard Python**: Use `if/else`, loops, functions - not custom DSLs
3. **Error Handling**: Always have a fallback plan
4. **Self-Correction**: Let agents fix their own mistakes with `ModelRetry`
5. **Production Ready**: Log, monitor, and handle edge cases

### When to Use PydanticAI

✅ **Use PydanticAI when**:
- Building production systems
- Need type safety
- Want transparent, debuggable code
- Prefer standard Python patterns

❌ **Don't use PydanticAI when**:
- Need built-in RAG (integrate separately)
- Need complex memory (build your own)
- Want maximum abstraction (use LangChain)
- Prototyping quickly (requires more setup)

---

## Next Steps

1. **Install PydanticAI**: `pip install pydantic-ai`
2. **Read the Docs**: https://ai.pydantic.dev/
3. **Try the Template**: Copy the production template above
4. **Build Something**: Start with a simple agent, then add complexity
5. **Learn Pydantic**: Understanding Pydantic is essential for PydanticAI

Remember: **Type safety + Standard Python + Error Handling = Production-Ready Agents**

---

## Additional Resources

- **PydanticAI Documentation**: https://ai.pydantic.dev/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Async Python**: https://docs.python.org/3/library/asyncio.html
- **Lockfire Integration**: Monitoring and debugging (similar to LangSmith/LangFuse) - check PydanticAI docs for latest updates

## Early Beta Considerations

### Current Status (As of 2024)

PydanticAI is in **early beta**. Here's what you need to know:

**What Works Well**:
- ✅ Core functionality (agents, dependencies, structured output)
- ✅ Tools and self-correction
- ✅ Streaming
- ✅ Type safety

**Known Limitations**:
- ⚠️ Model parameter configuration (temperature, top_p) is limited
- ⚠️ Some edge cases with message history + tools
- ⚠️ API may change before stable release
- ⚠️ Less documentation/examples than mature frameworks

**Recommendation for Production**:
1. **Use for prototypes** - Great for learning and experimentation
2. **Use for non-critical features** - Internal tools, demos, MVPs
3. **Wait for stable release** - Before migrating critical production systems
4. **Extract patterns** - Learn the dependency injection concept, apply it to your own code

**The PydanticAI Philosophy**:
> "Focus on structuring inputs and outputs in a way that makes them available for LLMs, rather than trying to solve all agent problems."

This is refreshing - it's a **focused tool** rather than trying to be everything to everyone.

---

**The Golden Rule**: If you can solve it with type-safe Python, use PydanticAI. If you need heavy abstractions, consider LangChain (but you'll lose type safety). And remember: frameworks are tools, not solutions. Stay flexible.
