# LangChain: From Zero to Hero - Complete Guide

**Your Mentor: Todd (Senior AI Engineer & Team Lead)**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Lessons](#lessons)
5. [Production Best Practices](#production-best-practices)
6. [Common Patterns](#common-patterns)

---

## Introduction

### What is LangChain?

LangChain is a **framework** for building applications powered by Large Language Models (LLMs). Think of it as a toolkit that provides:

- **Standardized interfaces** for working with different LLM providers (OpenAI, Anthropic, etc.)
- **Building blocks** (chains, agents, memory) for complex AI applications
- **Production-ready patterns** for error handling, retries, and monitoring
- **Integration** with data sources, vector databases, and tools

### Why LangChain?

**Without LangChain:**
```python
# Direct API calls - lots of boilerplate
import openai
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
# Manual error handling, retries, rate limiting...
```

**With LangChain:**
```python
# Clean, standardized interface
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")
response = llm.invoke([HumanMessage(content="Hello")])
# Built-in error handling, retries, etc.
```

---

## Installation & Setup

### Step 1: Install LangChain

```bash
pip install langchain langchain-openai langchain-community python-dotenv
```

**Production Tip:** Always pin versions in production:
```bash
pip install langchain==0.3.0 langchain-openai==0.2.0
```

### Step 2: Environment Setup

Create a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

**Never commit `.env` files to git!** Add to `.gitignore`:
```
.env
.env.local
```

### Step 3: Load Environment Variables

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

---

## Core Concepts

### 1. LLM vs ChatModel

**LLM (Legacy):**
- Text in → Text out
- Simpler but less structured
- Example: `llm("Hello")`

**ChatModel (Recommended):**
- Messages in → Messages out
- More structured, better for production
- Example: `chat_model.invoke([HumanMessage("Hello")])`

**Always use ChatModel for new projects!**

### 2. Messages

LangChain uses structured messages:

- `SystemMessage`: Sets the AI's role/behavior
- `HumanMessage`: User input
- `AIMessage`: AI responses
- `FunctionMessage`: Tool/function results

### 3. Invoke vs Stream

- `invoke()`: Get complete response (blocking)
- `stream()`: Get response chunks (for real-time UX)

---

## Lessons

### Lesson 1: Basic LLM Usage ✅

**File:** `lesson_01_basic_llm.py`

**What you'll learn:**
- Setting up ChatOpenAI
- Making your first call
- Using SystemMessages
- Error handling

**Key Code:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello!")
])
print(response.content)
```

**Questions for Eran:**
1. What's the difference between `temperature=0` and `temperature=1`?
2. Why do we use `SystemMessage` instead of putting instructions in `HumanMessage`?
3. What happens if the API key is invalid?

---

### Lesson 2: Prompt Templates (Coming Next)

**What you'll learn:**
- Creating reusable prompts
- Variable substitution
- Prompt versioning

---

### Lesson 3: Chains (Coming Next)

**What you'll learn:**
- Composing multiple operations
- Sequential chains
- Parallel execution

---

## Production Best Practices

### 1. Error Handling

**Always wrap LLM calls:**
```python
try:
    response = llm.invoke(messages)
except Exception as e:
    logger.error(f"LLM call failed: {e}")
    # Fallback logic or retry
```

### 2. Rate Limiting

LangChain handles retries automatically, but you can configure:
```python
llm = ChatOpenAI(
    model="gpt-4",
    max_retries=3,
    timeout=30
)
```

### 3. Logging

**Always log LLM interactions:**
```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"LLM Request: {messages}")
response = llm.invoke(messages)
logger.info(f"LLM Response: {response.content}")
```

### 4. Cost Management

- Use `gpt-4o-mini` for development/testing
- Monitor token usage
- Set usage limits in production

### 5. Security

- Never expose API keys
- Validate user inputs
- Sanitize outputs before displaying

---

## Common Patterns

### Pattern 1: Simple Q&A

```python
def ask_question(question: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke([HumanMessage(content=question)])
    return response.content
```

### Pattern 2: Role-Based Assistant

```python
def get_assistant_response(user_input: str, role: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(content=f"You are a {role}."),
        HumanMessage(content=user_input)
    ]
    response = llm.invoke(messages)
    return response.content
```

### Pattern 3: Streaming Response

```python
def stream_response(question: str):
    llm = ChatOpenAI(model="gpt-4o-mini")
    for chunk in llm.stream([HumanMessage(content=question)]):
        print(chunk.content, end="", flush=True)
```

---

## Next Steps

1. ✅ Complete Lesson 1
2. ⏭️ Move to Lesson 2: Prompt Templates
3. ⏭️ Lesson 3: Chains
4. ⏭️ Lesson 4: Memory
5. ⏭️ Lesson 5: RAG Basics

---

**Remember:** Production-grade code is:
- ✅ Well-tested
- ✅ Error-handled
- ✅ Logged
- ✅ Documented
- ✅ Secure

**Questions? Ask Todd!**
