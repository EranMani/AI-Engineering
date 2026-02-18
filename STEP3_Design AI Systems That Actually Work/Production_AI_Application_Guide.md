# Production-Grade AI Applications: A Beginner's Guide

> **For:** Junior AI engineers starting their first AI project.  
> **From:** Senior AI engineer perspective.  
> **Style:** Concise, simple, and practical. You don't need to memorize this—bookmark it and refer back.

---

## Start Here

**This guide is your roadmap.** You don't need to read it top-to-bottom right now. Use it like this:

| If you… | Do this |
|---------|---------|
| **Just got assigned to an AI project** | Read [Core Mindset](#core-mindset-deterministic-software-first) and [The 7 Blocks](#the-7-building-blocks-of-an-ai-application), then [Day 1 Checklist](#day-1-checklist-when-youre-assigned-to-a-project). |
| **Want to run something in 5 minutes** | Skip to [Run Your First Agent](#run-your-first-agent-in-5-minutes). |
| **Want to avoid API costs / work offline** | Skip to [Local Models & Ollama](#local-models--ollama). |
| **Need to implement a specific feature** | Use the [Quick Mental Model](#quick-mental-model) to find the right block, then jump to that section. |
| **Want the full picture** | Follow the [Learning Path](#learning-path-suggested-order). |

**You've got this.** Most production systems use only 3–4 of the 7 blocks at a time. Start small, add complexity as you need it.

---

## Table of Contents

### Read First (Essential)

1. [Core Mindset](#core-mindset-deterministic-software-first)
2. [The 7 Building Blocks](#the-7-building-blocks-of-an-ai-application)
3. [Run Your First Agent](#run-your-first-agent-in-5-minutes)
4. [Day 1 Checklist](#day-1-checklist-when-youre-assigned-to-a-project)
5. [Putting It All Together](#putting-it-all-together)

### Reference (When You Need It)

6. [Tools & Actionability](#tools--actionability)
7. [Structured Outputs](#structured-outputs)
8. [Using PydanticAI](#using-pydanticai-as-a-framework)
9. [Local Models & Ollama](#local-models--ollama)
10. [Asynchronous Execution](#asynchronous-execution)
11. [Observability & Error Handling](#observability--error-handling)
12. [Design Patterns](#design-patterns)

### Helpers

- [Common Questions](#common-questions)
- [Stuck? Try This](#stuck-try-this)
- [Quick Glossary](#quick-glossary)

---

## Core Mindset: Deterministic Software First

Before the code, one mindset shift that will save you a lot of pain:

**The golden rule:** An LLM call is the most expensive and least predictable operation in your system. Use it only when you need *reasoning with context* that code cannot do.

- **Most steps** in your workflows should be **regular code** (if/else, loops, API calls), not LLM calls.
- **Break big problems** into small steps. Solve with code first. Add LLM only where necessary.
- **Context engineering** is the fundamental skill: preparing the right context so the LLM can reliably solve your specific problem.

As you gain experience, you'll notice that the best AI systems feel like "normal software with a few smart steps"—not "an AI that does everything."

---

## The 7 Building Blocks of an AI Application

These blocks are the foundation of production-ready AI systems. Use them as a checklist.

| Block | Name | Purpose |
|-------|------|---------|
| **1** | **Intelligence** 🧠 | The LLM API call. The only truly "AI" part. |
| **2** | **Memory** 🗃️ | Storing and passing conversation history across turns. |
| **3** | **Tools** 🛠️ | Letting the LLM call functions (APIs, DB, etc.) in the real world. |
| **4** | **Validation** ✅ | Forcing the LLM to return structured data (e.g. JSON) with retries. |
| **5** | **Control** 🚦 | Classifying intent and routing with deterministic code. |
| **6** | **Recovery** 🛟 | Retries, backoff, and fallbacks when things fail. |
| **7** | **Feedback** 🛑 | Human approval for high-stakes actions (emails, payments, etc.). |

### Quick Mental Model

- **Need to understand the user?** → Block 1 (Intelligence) + Block 5 (Control)
- **Need to remember context?** → Block 2 (Memory)
- **Need to get real data?** → Block 3 (Tools)
- **Need reliable data shapes?** → Block 4 (Validation)
- **Need to handle failures?** → Block 6 (Recovery)
- **Need to be safe?** → Block 7 (Feedback)

---

## Run Your First Agent (in 5 Minutes)

**Why:** Seeing something work builds confidence. Run this before diving into theory.

Copy this into a file, add your OpenAI API key (or use `OPENAI_API_KEY` in `.env`), and run it:

```python
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 25 + 17? Reply with just the number."}
    ]
)
print(response.choices[0].message.content)  # You'll get: 42
```

**You just used Block 1 (Intelligence).** That's the foundation. Everything else builds on this.

**Next step:** Add memory so it can handle follow-up questions. See `code_examples/02_block2_memory_basic.py`.

---

## Day 1 Checklist (When You're Assigned to a Project)

Before writing code, do this:

1. **Understand the problem** — What does the user actually need? Single-turn or multi-turn?
2. **Decide which blocks you need** — Use the [Quick Mental Model](#quick-mental-model) above.
3. **Find the code examples** — Check `code_examples/` for `01_block1_*` through `07_block7_*`; there's likely something close to what you need.
4. **Start with the simplest version** — One block at a time. Get it working, then add.
5. **Ask your team** — Which framework are we using? (PydanticAI, vanilla OpenAI, etc.) Where is the API key configured?

---

## Learning Path (Suggested Order)

| Week | Focus | What to build |
|------|-------|---------------|
| **1** | Blocks 1–3 | Simple chatbot → add memory → add one tool (e.g. weather) |
| **2** | Blocks 4–5 | Add structured output → add intent classification & routing |
| **3** | Blocks 6–7 | Add retries → add human approval for sensitive actions |
| **4+** | Patterns | Study Router, Chain, Parallelization from `code_examples/18_*` onward |

---

## Tools & Actionability

**When to read this:** When your AI needs to fetch real data (weather, orders, DB) or perform actions. Skip for simple chat-only bots.

### Why Tools Matter

LLMs live in text. They cannot access databases, APIs, or the internet. **Tools** give them "hands" to act in the real world.

### How It Works (The "Ping-Pong" Loop)

1. **User:** "What's the weather in Paris?"
2. **LLM:** Decides to call `get_weather` with `city="Paris"`.
3. **Your code:** Executes `get_weather("Paris")` and gets real data.
4. **Your code:** Sends the result back to the LLM.
5. **LLM:** Uses that data to answer the user.

**Important:** The LLM never executes code. It returns a *request* to call a tool. Your code executes it.

### Vanilla OpenAI Example (from `03_block3_tools_basic.py`)

```python
# 1. Define the function
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

# 2. Describe it to the LLM (JSON schema)
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather of a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

# 3. Call LLM with tools
response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)

# 4. If LLM wants to use a tool, execute it and send the result back
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    result = get_weather(args["city"])
    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
    # Call LLM again with the tool result
```

### Key Takeaways

- Define clear tool descriptions so the LLM knows when to use them.
- Validate tool inputs (format, range) before executing.
- Never let tools do dangerous things without safeguards.

---

## Structured Outputs

**When to read this:** When you need the AI's response in a predictable format (e.g. to save to a DB or pass to other code). Skip if a plain text answer is fine for now.

### The Problem

LLMs return free-form text. Sometimes it's bullet points, sometimes paragraphs. Parsing with regex is fragile.

### The Solution

**Force the LLM to return JSON that matches a schema.** Use Pydantic (or similar) to validate and parse.

### Basic Pattern (from `08_pydanticai_structured_output.py`)

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class MovieResult(BaseModel):
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")

agent = Agent(model="gpt-4o", output_type=MovieResult)

result = agent.run_sync("What is the best movie of all time?")
print(result.output.title)   # Type-safe!
print(result.output.year)   # Validated integer!
```

### The "Self-Healing" Loop (Retry on Validation Fail)

If the LLM returns invalid JSON or violates rules:

1. **Catch** the validation error.
2. **Send the error** back to the LLM as a user message: *"Error: You used Chicken. Try again."*
3. **Retry** (with a max limit).

This turns validation failures into learning opportunities for the model.

### Key Takeaways

- Use Pydantic models (or equivalents) to define expected shapes.
- Use `response_format` in OpenAI or `output_type` in PydanticAI.
- Add retry logic when validation fails.
- Structured output is critical for production—downstream code depends on predictable data.

---

## Using PydanticAI as a Framework

**When to read this:** When your team uses PydanticAI, or when you want less boilerplate and built-in type safety. If you're using vanilla OpenAI, you can skip for now.

PydanticAI is a **lightweight, type-safe** framework for building AI agents. It focuses on:

- **Structured I/O** (inputs and outputs)
- **Tools** with easy registration
- **Dependency injection** for context
- **Standard Python** (no custom DSL)

### The 4 Pillars

| Pillar | Purpose |
|--------|---------|
| **1. Structured Output** | `result_type=MyModel` — the agent returns validated Pydantic models. |
| **2. Dependency Injection** | `deps_type=MyContext` — pass user, DB, API keys without string formatting. |
| **3. Tools & Self-Correction** | `@agent.tool` — register functions; use `ModelRetry` to ask the LLM to fix bad inputs. |
| **4. Streaming** | `agent.run_stream()` — stream text as it arrives for better UX. |

### Why PydanticAI Over Vanilla?

- **Less boilerplate:** Tools are registered with decorators; no manual JSON schemas.
- **Type safety:** Results are Pydantic models; no manual parsing.
- **Self-correction:** `ModelRetry` lets the LLM fix tool input errors automatically.
- **Retries:** Built-in retry logic for validation and tool failures.

### Quick Example

```python
from pydantic_ai import Agent, RunContext, ModelRetry

@dataclass
class UserContext:
    user_id: str
    subscription: str

agent = Agent('openai:gpt-4o', deps_type=UserContext, result_type=ResponseModel)

@agent.tool
def get_order_status(ctx: RunContext[UserContext], order_id: str) -> str:
    if not order_id.startswith("#"):
        raise ModelRetry("Order IDs must start with '#'")
    return f"Order {order_id}: Shipped"

result = agent.run_sync("What's my order #12345?", deps=UserContext(...))
```

See `17_pydanticai_vs_vanilla_comparison.md` and `PydanticAI_Production_Guide.md` for details.

---

## Local Models & Ollama

**When to read this:** When you want to avoid token costs, work offline, or prototype without API keys. Ollama runs models locally on your machine.

### Why Use Local Models?

| Benefit | Cloud (OpenAI, etc.) | Local (Ollama) |
|---------|----------------------|----------------|
| **Cost** | Pay per token | Free after setup |
| **Privacy** | Data sent to provider | Data stays on your machine |
| **Offline** | Requires internet | Works offline |
| **Latency** | Network round-trip | Often faster (local) |
| **Model choice** | Provider's models | Llama, Mistral, Gemma, etc. |

**Trade-off:** Local models are typically smaller and may be less capable than GPT-4/Claude. Use them for prototyping, simple tasks, or when cost matters. Use cloud models for complex reasoning or production when quality is critical.

### Setup: Install Ollama

1. **Install:** [ollama.com](https://ollama.com) → download for your OS  
2. **Pull a model:** Open a terminal and run:  
   `ollama pull llama3.2` (or `mistral`, `gemma2`, `phi3`, etc.)  
3. **Verify:** `ollama run llama3.2` — you should get a chat prompt.

Ollama exposes an **OpenAI-compatible API** at `http://localhost:11434/v1`, so you can use the same patterns as with OpenAI.

### Vanilla OpenAI Client + Ollama

Use the standard OpenAI client with `base_url` pointing at Ollama. No API key needed for local:

```python
from openai import OpenAI

# Point to local Ollama instead of OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama ignores this; use any placeholder for local
)

response = client.chat.completions.create(
    model="llama3.2",  # Use the model name you pulled (llama3.2, mistral, etc.)
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)
print(response.choices[0].message.content)
```

### PydanticAI + Ollama

PydanticAI has built-in **OllamaProvider** support. Use the `ollama:` prefix or configure explicitly:

**Option 1: Shorthand (with env vars)**

```bash
# Optional: set if Ollama runs elsewhere
export OLLAMA_BASE_URL="http://localhost:11434/v1"
```

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class MovieResult(BaseModel):
    title: str = Field(description="The movie title")
    year: int = Field(description="Release year")

# Use ollama:model-name — same agent API as OpenAI
agent = Agent("ollama:llama3.2", output_type=MovieResult)

result = agent.run_sync("What is the best movie of all time?")
print(result.output.title, result.output.year)
```

**Option 2: Explicit configuration (no env vars)**

```python
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

class MovieResult(BaseModel):
    title: str
    year: int

# Configure Ollama explicitly
ollama_model = OpenAIChatModel(
    model_name="llama3.2",  # or mistral, gemma2, phi3, etc.
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

agent = Agent(ollama_model, output_type=MovieResult)
result = agent.run_sync("Tell me about Inception")
print(result.output)  # MovieResult(title='Inception', year=2010)
```

### Tools, Memory, and Structured Output — Same as Cloud

Ollama models work with the same PydanticAI patterns: tools, dependency injection, structured output, and streaming. Swap the model; the rest of your agent code stays the same.

```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

ollama_model = OpenAIChatModel(
    model_name="llama3.2",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

agent = Agent(ollama_model, result_type=str)

@agent.tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Weather in {city}: Sunny, 22°C"

result = agent.run_sync("What's the weather in Paris?")
```

### Popular Ollama Models (as of 2025)

| Model | Size | Best for |
|-------|------|----------|
| `llama3.2` | 3B | Fast, lightweight chat |
| `mistral` | 7B | Good balance of speed and quality |
| `gemma2` | 2B | Very fast, simple tasks |
| `phi3` | 3.8B | Strong for its size |
| `llama3.1` | 8B | Better reasoning, slower |

Run `ollama list` to see what you have installed.

### Hybrid Strategy: Local for Dev, Cloud for Prod

Use Ollama locally during development (no cost, fast iteration). Switch to OpenAI/Anthropic for production when you need stronger models. Same agent code—only the model configuration changes.

```python
import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.ollama import OllamaProvider

def get_model():
    if os.getenv("USE_LOCAL_MODEL", "false").lower() == "true":
        return OpenAIChatModel(
            model_name="llama3.2",
            provider=OllamaProvider(base_url="http://localhost:11434/v1")
        )
    return OpenAIChatModel(
        model_name="gpt-4o",
        provider=OpenAIProvider()  # Uses OPENAI_API_KEY from env
    )

agent = Agent(get_model(), result_type=MyResult)
# USE_LOCAL_MODEL=true python app.py  → Ollama
# python app.py                        → OpenAI
```

📁 See `code_examples/29_ollama_pydanticai_agent.py` for a complete runnable example.

---

## Asynchronous Execution

**When to read this:** When you have multiple independent LLM or API calls and want to speed things up. Not needed for simple one-call-at-a-time flows.

LLM calls are slow (often 1–5 seconds). When you have **independent tasks**, run them **in parallel** instead of one after another.

### Sequential vs Parallel

**Sequential (slow):**
```python
# 9 seconds total
review1 = await review_security(code)      # 3 sec
review2 = await review_performance(code)   # 3 sec
review3 = await review_style(code)         # 3 sec
```

**Parallel (fast):**
```python
# ~3 seconds total
results = await asyncio.gather(
    review_security(code),
    review_performance(code),
    review_style(code)
)
```

### Example (from `19_pattern_parallelization.py`)

```python
async def main():
    reviewers = [
        create_reviewer_agent("Security", "vulnerabilities"),
        create_reviewer_agent("Performance", "speed and memory"),
        create_reviewer_agent("Maintainability", "readability"),
    ]
    tasks = [reviewer.run(bad_code) for reviewer in reviewers]
    results = await asyncio.gather(*tasks)  # All run at once
```

### When to Use Async

- ✅ Independent LLM calls or API calls
- ✅ Multiple tools that can run concurrently

### When NOT to Use

- ❌ Tasks depend on each other (A → B → C) — use a chain instead
- ❌ Rate limits or API constraints prevent parallel calls

---

## Observability & Error Handling

**When to read this:** Before deploying to production. Retries and fallbacks are essential; logging helps you debug when things break.

Things will fail: APIs down, rate limits, bad outputs. Handle failures gracefully.

### 1. Retry with Exponential Backoff (from `06_block6_recovery_retry.py`)

```python
MAX_RETRIES = 3

def get_response_with_retry(history):
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(model="gpt-4o", messages=history)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}. Retry {attempt + 1}/{MAX_RETRIES}")
            if attempt == MAX_RETRIES - 1:
                return None  # Fallback
```

### 2. Layered Recovery

1. **Retry** with backoff (for transient errors)
2. **Fallback function** (e.g., cached response, simpler logic)
3. **Hardcoded fallback** (user-friendly message)

### 3. Observability Basics

- **Log** each LLM call: inputs, outputs, token usage, latency
- **Track** errors and retries
- **Monitor** cost and usage for cost control

### 4. User-Friendly Errors

Never expose raw exceptions to users. Return messages like:

- *"I'm having trouble right now. Please try again later."*
- *"I couldn't process your request. Please rephrase or contact support."*

---

## Design Patterns

**When to read this:** When you're building something more complex (routing, multi-agent flows, parallel tasks). Start with Router and Chain—they're the most common.

Patterns are reusable ways to structure AI systems. Here are the main ones.

### Router Pattern 🚦

**Use when:** You need to classify intent and route to specialists.

```
User query → Classifier Agent → Route to Specialist Agent
```

- Use a **small, fast model** for classification.
- Use **if/else** (or `match`) for routing.

### Strategy Pattern 🎩

**Use when:** Behavior must depend on user context (tier, role, permissions).

- Free users get limited tools; premium users get full tools.
- Select agent config based on `User.tier` or `User.role`.

### Parallelization Pattern 🏎️

**Use when:** Tasks are independent.

- `asyncio.gather()` for multiple LLM calls.
- Cuts total time roughly to the slowest single task.

### Chain of Responsibility Pattern ⛓️

**Use when:** Steps depend on each other (A → B → C).

```
Research → Plan → Write → Edit
```

Output of each step becomes input to the next.

### Prompt Chaining Pattern 🧵

**Use when:** You need iterative refinement.

```
Draft → Critique → Refine
```

Pass previous output and critique into the next prompt.

### Evaluator-Optimizer Pattern 🧐

**Use when:** Output must meet a quality bar.

```
Generate → Evaluate (score) → If score < threshold, retry with feedback
```

### Facade Pattern 💼

**Use when:** You want one simple interface hiding many agents.

- One “Manager” agent with tools that call internal specialist agents.
- User only talks to the Manager.

See `AI_DESIGN_PATTERNS_GUIDE.md` and the `18_*` through `25_*` example files for more detail.

---

## Putting It All Together

### Your First Real Task: Build a Support Bot (Minimal Version)

Start with just 3 blocks. Add more later.

| Step | Block | What to do |
|------|-------|------------|
| 1 | **Intelligence** | Send user message to LLM, get response. (You did this in "Run Your First Agent.") |
| 2 | **Memory** | Store each user + assistant message in a list. Send the full list with each new request. |
| 3 | **Recovery** | Wrap the LLM call in `try/except`. On failure, return a friendly message like "I'm having trouble. Try again." |

Once that works: add **Tools** (e.g. `get_order_status`) and **Validation** (structured response schema). See `code_examples/` for patterns.

### A Simple Checklist for New Features

1. **Decompose** the problem into small steps.
2. **Assign blocks** to each step (Intelligence, Tools, Validation, etc.).
3. **Prefer code** where logic is deterministic.
4. **Use LLMs** where you need reasoning with context.
5. **Add recovery** (retries, fallbacks).
6. **Add feedback** (human approval) for risky actions.

### Example Flow: Customer Support (Full System)

```
User message
    → Block 5 (Control): Classify intent (Question / Complaint / Request)
    → Block 2 (Memory): Load conversation history
    → Block 3 (Tools): Maybe call get_order_status, check_invoice
    → Block 1 (Intelligence): Generate response
    → Block 4 (Validation): Ensure response matches schema
    → Block 6 (Recovery): Retry on failure, fallback message
    → Block 7 (Feedback): If escalation, wait for human approval
    → Block 2 (Memory): Save new messages
```

---

## Common Questions

| Question | Short Answer |
|----------|--------------|
| **Do I need all 7 blocks?** | No. Most apps use 3–4: Intelligence, Memory, Tools, and either Validation or Control. |
| **Where do I even start?** | Run the [5-minute agent](#run-your-first-agent-in-5-minutes), then add memory (Block 2). |
| **What if I'm just building a simple chatbot?** | Blocks 1 + 2 (Intelligence + Memory). Add Block 6 (Recovery) for production. |
| **When do I need Tools?** | When the AI must access real data (DB, APIs, files). If it's just conversation, you might not need them yet. |
| **PydanticAI or vanilla OpenAI?** | PydanticAI = less boilerplate, type safety. Vanilla = more control, more code. See `17_pydanticai_vs_vanilla_comparison.md`. |
| **When to use local (Ollama) vs cloud models?** | **Local:** Prototyping, cost-sensitive, offline, simple tasks. **Cloud:** Production, complex reasoning, best quality. You can use both: local for dev, cloud for prod. |
| **This feels overwhelming.** | Focus on Blocks 1–3 first. The rest is "add when you need it." |

---

## Stuck? Try This

| Symptom | What to try |
|---------|-------------|
| **Output is random or wrong** | Add **structured output** (Block 4). Define a Pydantic model for the response shape. |
| **Bot doesn't remember the conversation** | Add **memory** (Block 2). Pass the full message history with each request. |
| **Bot can't access real data** | Add **tools** (Block 3). Define a function, describe it to the LLM, execute it when the LLM requests it. |
| **App crashes when LLM fails** | Add **recovery** (Block 6). Wrap calls in `try/except`, retry with backoff, return a fallback message. |
| **Need to route to different logic** | Add **control** (Block 5). Classify intent first, then `if/else` to route. |
| **Too slow** | If you have independent tasks, use **async** with `asyncio.gather()`. |
| **Want to avoid API costs** | Use [Local Models (Ollama)](#local-models--ollama) for prototyping and development. |

---

## Quick Glossary

| Term | Meaning |
|------|---------|
| **LLM** | Large Language Model (e.g. GPT-4). Takes text in, returns text out. |
| **Context** | The text (prompts, history, docs) you send to the LLM. "Context engineering" = preparing it well. |
| **Tool / Function calling** | A function your code runs when the LLM requests it (e.g. get weather, query DB). |
| **Structured output** | Forcing the LLM to return JSON matching a schema (e.g. Pydantic model) instead of free text. |
| **Token** | Roughly 4 characters of text. LLMs have context limits (e.g. 128k tokens). |
| **ModelRetry** | (PydanticAI) Tell the LLM it made a mistake so it can fix and retry. |
| **Streaming** | Sending the response token-by-token as it's generated (typewriter effect). |
| **Ollama** | Tool to run LLMs locally. Exposes an OpenAI-compatible API at `localhost:11434`. No API key needed. |

---

## Summary

| Topic | One-Line Takeaway |
|-------|-------------------|
| **Tools** | LLMs request tool calls; your code executes them and returns results. |
| **Structured Output** | Force JSON schema + validation. Use retries when validation fails. |
| **PydanticAI** | Type-safe framework with tools, deps, and self-correction. |
| **Async** | Use `asyncio.gather()` for independent tasks to save time. |
| **Observability & Errors** | Retry with backoff, log everything, return user-friendly fallbacks. |
| **Design Patterns** | Router, Strategy, Parallel, Chain, Evaluator-Optimizer, Facade. |
| **7 Blocks** | Intelligence, Memory, Tools, Validation, Control, Recovery, Feedback. |

---

## Further Reading

### Start With (Run the Code)

| Resource | What you'll learn |
|----------|-------------------|
| `code_examples/01_block1_intelligence_simple.py` | Your first LLM call |
| `code_examples/02_block2_memory_basic.py` | Adding conversation memory |
| `code_examples/03_block3_tools_basic.py` | Letting the AI call functions |
| `code_examples/29_ollama_pydanticai_agent.py` | Local models with Ollama (no API key) |

### Go Deeper (When You're Ready)

| Resource | When to read |
|----------|--------------|
| `The_7_Foundational_Building_Blocks_Guide.md` | Full explanation of each block with examples |
| `PydanticAI_Production_Guide.md` | Using PydanticAI for type-safe agents |
| `17_pydanticai_vs_vanilla_comparison.md` | PydanticAI vs vanilla OpenAI |
| `AI_DESIGN_PATTERNS_GUIDE.md` | Router, Chain, Parallelization, and more |
| `code_examples/18_pattern_*` through `25_pattern_*` | Runnable pattern examples |

---

*Focus on these fundamentals rather than chasing new frameworks. These blocks and patterns are what most production AI systems are built on. You'll learn more by building one small thing at a time.*
