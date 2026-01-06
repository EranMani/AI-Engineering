# OpenAI Python SDK: Beginner → Master Playbook (AI Engineer Track)

> Quick note: I’m not Sam Altman (and can’t impersonate real people). But I *can* teach you the OpenAI Python SDK in a “CEO-level clarity” way: practical, production-minded, and interview-ready.

This guide focuses on the **OpenAI Python SDK** skills most AI engineering roles expect:
- secure **authentication**
- making **Requests** (especially **Responses API**)
- **streaming**
- **structured outputs** (JSON mode + JSON Schema / `text.format`)
- **tool calling** patterns
- **error handling**, **retries**, **timeouts**, and **logging**
- **async** + production “hygiene” (secrets, tests, observability)

---

## 0) Prereqs (minimum you need)

- Python **3.9+**
- Comfort with:
  - running terminal commands
  - creating a virtual environment
  - basic Python functions + dictionaries

---

## 1) Install the SDK (and keep your project clean)

### 1.1 Create a virtual environment (recommended)

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### 1.2 Install OpenAI SDK

```bash
pip install openai
```

> Tip: In real projects, pin versions (`pip freeze > requirements.txt`) so deployments are reproducible.

---

## 2) Authentication the right way (what hiring managers look for)

### 2.1 Set your API key as an environment variable

**macOS / Linux**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

**Windows PowerShell**
```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

### 2.2 Don’t leak keys

- ✅ Keep keys in environment variables, a secrets manager, or `.env` (ignored by git)
- ❌ Never commit keys to GitHub
- ❌ Never ship keys to client-side code (browser/mobile app)

**Recommended `.gitignore`**
```gitignore
.env
.venv/
__pycache__/
```

### 2.3 Quick sanity check script

Create `sanity_check.py`:

```python
import os

key = os.environ.get("OPENAI_API_KEY")
print("Key loaded:", bool(key))
print("Key prefix:", (key or "")[:7])
```

Run:
```bash
python sanity_check.py
```

If `Key loaded: False`, your environment variable is not set in that shell session.

---

## 3) Your first real request (Responses API)

The SDK’s **primary** generation API is the **Responses API**.

Create `hello_openai.py`:

```python
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY automatically

response = client.responses.create(
    model="gpt-5.2",
    input="Write a one-sentence bedtime story about a unicorn.",
)

print(response.output_text)
```

Run:
```bash
python hello_openai.py
```

### 3.1 What’s happening here?

- `OpenAI()` creates a client configured from your environment
- `responses.create(...)` sends a request
- `response.output_text` is a helper that returns the model’s final text output

---


---

## 3.5) When to use `responses` vs `chat.completions` (important)

OpenAI supports **both** APIs, but they’re best suited to different situations.

### Use **Responses** (`client.responses.create`) when…

This is the **recommended default for new projects**. citeturn1view2turn1view3

Pick Responses if you want any of these “modern platform” wins:
- **New projects** (the docs explicitly recommend starting here). citeturn1view2turn1view3  
- **Easier conversation chaining / state** via `previous_response_id` (or integrations with the Conversations API). citeturn1view1  
- A more “agentic” loop (built for **reasoning + acting + tools**). citeturn1view4  
- **Structured Outputs** with JSON Schema using `text.format` (Responses shape is the “new” shape). citeturn1view1  
- You want a cleaner response object + helper like `response.output_text`. citeturn1view1  

**Typical AI engineer use cases:** product chat, RAG assistants, extraction pipelines, agents that call tools, multimodal apps.

Minimal example (Responses):

```python
from openai import OpenAI
client = OpenAI()

r = client.responses.create(
    model="gpt-5",
    input="Write one sentence about otters.",
)
print(r.output_text)
```

### Use **Chat Completions** (`client.chat.completions.create`) when…

Choose Chat Completions if:
- You have an **existing codebase** (or library/framework) already built around `/v1/chat/completions` and you want minimal refactor. citeturn1view1  
- You prefer the older **messages → choices[0].message.content** shape for compatibility.
- You’re integrating with third-party tooling that expects Chat Completions request/response JSON.

Key tradeoff: Chat Completions is **stateless** — you must send the full message history every call (Responses supports easier chaining/state). citeturn1view1turn1view4

Minimal example (Chat Completions), straight from the migration guide:

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ],
)

print(completion.choices[0].message.content)
```
citeturn1view1

### A quick decision rule (use this in interviews)

- **Building something new?** Start with **Responses**. citeturn1view2turn1view3  
- **Maintaining an existing chat-completions app?** Stay on **Chat Completions** until you have time to migrate. citeturn1view1  
- **Need better tool/state support or structured JSON schema output?** Use **Responses**. citeturn1view1turn1view4  

---


## 4) Understanding responses (so you can debug and build products)

### 4.1 Extract the “assistant text” the simple way

```python
print(response.output_text)
```

### 4.2 Keep the whole response (you’ll want it in production)

Always log these in real services:
- the request ID (`response._request_id`)
- your “business-level” user ID (from your system)
- latency, retries, errors

```python
print("request_id:", response._request_id)
```

---

## 5) Prompt structure that scales

The Responses API supports:
- a simple `input="..."` shortcut
- or a full list of message items with typed content parts

### 5.1 Simple (fastest to learn)

```python
client.responses.create(
    model="gpt-5.2",
    input="Summarize this text: ...",
)
```

### 5.2 With system-style “instructions”

```python
client.responses.create(
    model="gpt-5.2",
    instructions="You are a strict code reviewer. Reply with bullet points only.",
    input="Review this function: ...",
)
```

---

## 6) Conversation state (multi-turn apps)

For multi-turn experiences you usually need to **persist context**.

Two common patterns:

### Pattern A — “manual history” (classic)

You store conversation messages yourself and send them each time.

### Pattern B — “chain responses” (simple with Responses)

You can chain using `previous_response_id` (the platform supports chaining responses this way).

Conceptually:

```python
r1 = client.responses.create(
    model="gpt-5.2",
    input="Remember: my favorite color is blue."
)

r2 = client.responses.create(
    model="gpt-5.2",
    previous_response_id=r1.id,
    input="What is my favorite color?"
)

print(r2.output_text)
```

> In production, you’ll store `response.id` per user/session.

---

## 7) Streaming (critical for UX + many interviews)

### 7.1 Why stream?
- Better UX (“it’s alive”)
- Lower perceived latency
- Enables partial updates (progress bars, token-by-token display)

### 7.2 Streaming example (basic pattern)

The exact streaming interface can vary by SDK version, but the core idea is:

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.stream(
    model="gpt-5.2",
    input="Explain recursion like I'm five.",
)

for event in stream:
    # You typically handle text deltas here
    # e.g., print(event.delta, end="")
    pass
```

If your SDK version doesn’t expose `responses.stream`, use the **Streaming** guide in the docs and match your installed SDK.

---

## 8) Structured Outputs (this is the “AI engineer” differentiator)

If you want the model to return **machine-safe JSON** (not “JSON-ish”), you have two levels:

### Level 1 — JSON mode (valid JSON, no schema guarantee)

Use when:
- you just need valid JSON
- schema strictness is not mission-critical

### Level 2 — Structured Outputs with JSON Schema (recommended)

Use when:
- you need JSON that **matches a schema**
- you’re building UI, pipelines, or downstream automation
- reliability matters

---

## 9) Structured Outputs with JSON Schema (Responses API)

In the Responses API, Structured Outputs live under:

```python
text={
  "format": {
     "type": "json_schema",
     "strict": True,
     "schema": {...}
  }
}
```

### 9.1 Example: extract tasks from a paragraph

```python
from openai import OpenAI

client = OpenAI()

task_schema = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "due_date": {"type": "string", "description": "ISO date like 2026-01-04"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["title", "priority"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["tasks"],
    "additionalProperties": False,
}

response = client.responses.create(
    model="gpt-5.2",
    input="Turn this into tasks: Buy milk tomorrow. Submit report next Monday. Call mom.",
    text={
        "format": {
            "type": "json_schema",
            "strict": True,
            "schema": task_schema,
        }
    },
)

# output_text will now be JSON text
print(response.output_text)
```

### 9.2 Parse it safely

```python
import json

data = json.loads(response.output_text)
print(data["tasks"][0]["title"])
```

### 9.3 Pro move: validate with Pydantic (interview gold)

```bash
pip install pydantic
```

```python
from pydantic import BaseModel, Field
from typing import List, Literal

class Task(BaseModel):
    title: str
    due_date: str | None = None
    priority: Literal["low", "medium", "high"]

class TaskList(BaseModel):
    tasks: List[Task]

parsed = TaskList.model_validate_json(response.output_text)
print(parsed.tasks)
```

---

## 10) Tool calling (functions) vs Structured Outputs

Use **tool calling** when the model should call *your code*.
Use **Structured Outputs** when the model should return JSON to *you*.

### 10.1 Tool calling mental model

1) You provide a tool schema (function name + params)
2) Model decides to call it (or not)
3) You run the function
4) You send results back so the model can finalize an answer

Tool calling is a big topic — but the workflow is always the same.

---

## 11) Vision inputs (images) with the Python SDK

If your product involves images, learn this early.

### 11.1 Image URL input

```python
from openai import OpenAI

client = OpenAI()

prompt = "What is in this image?"
img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/2023_06_08_Raccoon1.jpg/1599px-2023_06_08_Raccoon1.jpg"

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": img_url},
            ],
        }
    ],
)

print(response.output_text)
```

---

## 12) Production-grade reliability: errors, retries, timeouts, request IDs

This is where beginners become “hireable”.

### 12.1 Robust error handling template

```python
import openai
from openai import OpenAI

client = OpenAI()

try:
    resp = client.responses.create(model="gpt-5.2", input="Say hello.")
    print(resp.output_text)
    print("request_id:", resp._request_id)

except openai.APIConnectionError as e:
    print("Network problem / timeout / DNS:", e)

except openai.RateLimitError as e:
    print("Rate limited (429). Back off + retry:", e)

except openai.APIStatusError as e:
    print("Non-2xx status code:", e.status_code)
    print("Response body:", e.response)
    print("request_id:", e.request_id)
```

### 12.2 Configure retries

```python
from openai import OpenAI

client = OpenAI(max_retries=0)  # disable retries (sometimes useful)

# or per-request
client.with_options(max_retries=5).responses.create(
    model="gpt-5.2",
    input="Write a haiku about retries.",
)
```

### 12.3 Configure timeouts

```python
import httpx
from openai import OpenAI

client = OpenAI(timeout=20.0)  # 20 seconds

client = OpenAI(timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0))
```

### 12.4 Enable SDK logging

```bash
export OPENAI_LOG=info
# or
export OPENAI_LOG=debug
```

---

## 13) Async usage (common in web backends)

If you’re building FastAPI / async services, learn this.

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    r = await client.responses.create(
        model="gpt-5.2",
        input="Explain async/await in one paragraph."
    )
    print(r.output_text)

asyncio.run(main())
```

---

## 14) “Master-level” SDK patterns (what real teams do)

### 14.1 Wrap the SDK in your own service layer

You want:
- one place to control model choice
- one place for retries/timeouts
- structured logs
- consistent schema validation

Example skeleton:

```python
from dataclasses import dataclass
from openai import OpenAI

@dataclass
class LLMConfig:
    model: str = "gpt-5.2"
    timeout_s: float = 20.0
    max_retries: int = 2

class LLMService:
    def __init__(self, config: LLMConfig):
        self.client = OpenAI(timeout=config.timeout_s, max_retries=config.max_retries)
        self.model = config.model

    def draft(self, prompt: str) -> str:
        r = self.client.responses.create(model=self.model, input=prompt)
        return r.output_text
```

### 14.2 Always validate structured outputs

Rule of thumb:
- **If code depends on fields, validate.**
- If it’s just text to a human, you can be flexible.

### 14.3 Disable storage when needed

Some apps require not storing responses. The platform lets you set `store: false` for Responses.

---

## 15) Practice path: from zero → job-ready

### Week 1: Core SDK literacy
- Install + auth + first request
- Extract output text, log request IDs
- Handle errors + timeouts

### Week 2: Structured outputs + validation
- JSON mode
- JSON Schema Structured Outputs with `strict: true`
- Pydantic parsing
- Build a mini “data extraction” service

### Week 3: Streaming + async
- Stream responses in a CLI
- AsyncOpenAI in a FastAPI endpoint

### Week 4: A portfolio project (strong signal for AI engineer roles)
Build a small service that:
- accepts a user message (HTTP API)
- returns **validated JSON** that your UI can render
- uses retries/timeouts
- logs request IDs + latency
- includes tests for schema validation and failure modes

---

## Appendix: Official sources (URLs)

```text
https://platform.openai.com/docs/quickstart
https://platform.openai.com/docs/api-reference/responses
https://github.com/openai/openai-python
https://platform.openai.com/docs/guides/structured-outputs
https://platform.openai.com/docs/guides/migrate-to-responses
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
https://platform.openai.com/docs/guides/tools
```
