# The 7 Pillars of AI Engineering: Foundation Level

**Status:** ✅ Completed

> This document outlines the fundamental architecture of building reliable, controlled, and intelligent applications using Large Language Models (LLMs). These concepts move beyond simple "prompting" into true software engineering.

---

## Table of Contents

1. [Intelligence (The Brain)](#1-intelligence-the-brain)
2. [Memory (The Context)](#2-memory-the-context)
3. [Tools (The Hands)](#3-tools-the-hands)
4. [Validation (The Structure)](#4-validation-the-structure)
5. [Control (The Router)](#5-control-the-router)
6. [Recovery (The Shield)](#6-recovery-the-shield)
7. [Feedback (The Gate)](#7-feedback-the-gate)
8. [How They Work Together](#how-they-work-together)

---

## 1. Intelligence (The Brain)

**Concept:** The basic API call that sends text to the LLM and receives a response.

**Why:** To access the reasoning and generation capabilities of the model.

**How:** Using `client.chat.completions.create()` method.

**When:** Every time you need the AI to think, write, or analyze data.

**Key Insight:** The LLM is **stateless**. It remembers nothing between two separate calls unless you provide context.

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 2. Memory (The Context)

**Concept:** Manually managing the conversation history to create the illusion of a continuous chat.

**Why:** LLMs have no long-term memory. Without this, the AI forgets your name the moment you send the next message.

**How:**

1. Create a list: `history = [{"role": "system", ...}]`
2. Append user input: `history.append({"role": "user", "content": ...})`
3. Send the entire list to the API
4. Append AI response: `history.append({"role": "assistant", "content": ...})`

**When:** Any chatbot, assistant, or multi-turn workflow.

**Implementation Pattern:**

```python
history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# User message
history.append({"role": "user", "content": user_input})

# AI response
response = client.chat.completions.create(model="gpt-4", messages=history)
history.append(response.choices[0].message)
```

---

## 3. Tools (The Hands)

**Concept:** Giving the AI the ability to execute code or call external APIs (like `get_weather` or `query_database`).

**Why:** LLMs are trapped in a text box. They cannot see the time, check stock prices, or send emails on their own.

**How:** You define a JSON schema for a function, pass it to the LLM, and if the LLM decides to "call" it, your code executes the actual function and feeds the result back.

**When:** When the AI needs real-time data or needs to perform an action in the real world.

**Key Pattern:**

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather of a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"}
            },
            "required": ["city"]
        }
    }
}]

# When AI calls a tool, response.content is usually None
# Check response.choices[0].message.tool_calls instead
```

**Critical Note:** When the AI calls a tool, `.content` is usually `None`. Always check `tool_calls` first.

---

## 4. Validation (The Structure)

**Concept:** Forcing the AI to output data in a strict format (like JSON or Pydantic models) instead of free text.

**Why:** You cannot code against a paragraph of text. You need structured data (variables, booleans, integers) to build reliable software.

**How:** Using `response_format` with Pydantic classes (`BaseModel`).

**When:** Extracting data, classifying inputs, or populating databases.

**Example:**

```python
from pydantic import BaseModel, Field

class UserInfo(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(description="User's age in years")

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    response_format={"type": "json_schema", "json_schema": {
        "name": "user_info",
        "strict": True,
        "schema": UserInfo.model_json_schema()
    }}
)
```

**Secret Weapon:** Putting logic inside `Field(description="...")` is often more powerful than system prompts.

---

## 5. Control (The Router)

**Concept:** Using the AI to classify intent, then using standard Python code (`if/else`) to route the request.

**Why:** Not every query needs the same handling. Some are high-risk, some are low-risk. Some need a database, some need a calculator.

**How:**

1. Ask LLM to classify input (e.g., `risk_score`, `intent`)
2. Use Python `if/else` to direct the flow based on that classification

**When:** Building complex systems that handle multiple types of user requests (e.g., Customer Support bots).

**Pattern:**

```python
# Classify first
classification = classify_user_intent(user_input)

# Route based on classification
if classification.risk_score > 0.8:
    route_to_human_review()
elif classification.intent == "refund":
    process_refund_workflow()
else:
    handle_general_query()
```

---

## 6. Recovery (The Shield)

**Concept:** Building resilience against crashes, outages, and hallucinations.

**Why:** APIs fail. LLMs make mistakes. A production system cannot crash just because the internet blinked.

**How:**

- **Retry Loops:** `while` loops that catch errors and retry
- **Transient Memory:** Using temporary history lists during retries to avoid polluting the main database with error logs
- **Defense in Depth:** Layer 1 (LLM) → Layer 2 (Simple Algorithm) → Layer 3 (Hardcoded Error)

**When:** **ALWAYS.** Every production system requires error handling.

**Layered Recovery Strategy:**

```python
def safe_llm_call(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(...)
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                # Layer 3: Hardcoded fallback
                return fallback_response()
            # Layer 2: Simple retry with exponential backoff
            time.sleep(2 ** attempt)
    return None
```

---

## 7. Feedback (The Gate)

**Concept:** "Human-in-the-Loop" — pausing execution to get human approval before performing dangerous actions.

**Why:** AI is probabilistic, not deterministic. It will eventually mess up. You don't want it sending a refund of $50,000 or deleting a database without permission.

**How:**

1. **Drafting:** AI creates the Draft object
2. **Gating:** System pauses for `input("Approve? y/n")`
3. **Execution:** Action only happens if human types 'y'
4. **Edit Loop:** Allowing the human to refine the draft (`yes/no/edit`) before approval

**When:** High-stakes actions (money, public communication, destructive commands).

**Workflow:**

```python
# 1. AI creates draft
draft = ai_generate_refund_request(user_id, amount)

# 2. Gate: Human approval required
approval = input(f"Approve refund of ${draft.amount}? (y/n/edit): ")

if approval == "y":
    execute_refund(draft)
elif approval == "edit":
    # Edit loop: refine and re-approve
    draft = edit_draft(draft)
    # Re-enter approval gate
```

---

## How They Work Together

A complete AI Agent combines all these blocks into a single pipeline:

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Memory    │ ← Appends to history
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Control   │ ← Classifies intent (is this dangerous?)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Tools    │ ← Gathers extra data (if needed)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Intelligence │ ← Generates response/action plan
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validation  │ ← Ensures response follows strict schema
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Recovery   │ ← Retries if API fails or schema is wrong
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Feedback   │ ← Pauses for human approval (if high-risk)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Action    │ ← Finally executed
└─────────────┘
```

### Complete Flow Example

1. **User Input** arrives → "Refund $500 to customer 12345"
2. **Memory** appends it to history
3. **Control** classifies the intent → `risk_score: 0.9` (high-risk)
4. **Tools** gather customer data → `get_customer_info(12345)`
5. **Intelligence** generates a response/action plan → Draft refund request
6. **Validation** ensures the response follows the strict schema → `RefundRequest` model
7. **Recovery** retries if the API fails or the schema is wrong → 3 attempts max
8. **Feedback** pauses and asks the human for permission → `input("Approve? y/n")`
9. **Action** is finally executed → `process_refund()` only if approved

---

## Key Takeaways

- **Intelligence** is stateless — always provide context
- **Memory** must be manually managed — append every message
- **Tools** extend capabilities — but check `tool_calls`, not `content`
- **Validation** ensures structure — use Pydantic models
- **Control** routes intelligently — classify first, then route
- **Recovery** is mandatory — always handle failures gracefully
- **Feedback** prevents disasters — gate high-risk actions

**Remember:** These aren't optional features. They're the foundation of production-ready AI systems.
