# The 7 Foundational Building Blocks: A Complete Guide for Junior AI Engineers

## Introduction: Calm Your AI Anxiety

If you're a developer looking at your LinkedIn or X feeds right now, you're likely overwhelmed. Everyone is talking about "AI Agents," new frameworks drop every week (LangChain, LlamaIndex, etc.), and tutorials seem contradictory or broken.

**Here's the secret senior engineers know: You can ignore 99% of the tools you see online.**

After trying countless agent frameworks and talking to developers building real AI products, here's what becomes clear: **the frameworks aren't being used in production.**

Most successful AI applications are built with custom building blocks, not frameworks. This is because most effective "AI agents" aren't actually that agentic at all. They're mostly deterministic software with strategic LLM calls placed exactly where they add value.

The problem is that most frameworks push the "give an LLM some tools and let it figure everything out" approach. But in reality, you don't want your LLM making every decision. You want it handling the one thing it's good at - **reasoning with context** - while your code handles everything else.

The best teams in the world aren't using "magic" agent frameworks; they're using custom building blocks based on standard software engineering. This guide will strip away the hype and teach you the **7 Foundational Building Blocks** you need to build production-ready systems using any programming language (Python, TypeScript, Java, etc.).

### Personal Assistants vs. Background Automation

There's a huge difference between building **personal assistants** (like ChatGPT, Cursor) where users are in the loop, versus building **fully automated systems** that process information or handle workflows without human intervention. 

Most of you aren't building the next ChatGPT - you're building **background automations** to make your work or company more efficient. This distinction matters because it affects how you design your system, where you place LLM calls, and how much human oversight you need.

---

## The Core Philosophy: Deterministic Software > Magic

Before we touch the code, you must understand the mindset shift. A "hype" agent tries to do everything with one prompt. A "reliable" agent is just deterministic software with strategic LLM calls placed exactly where they add value.

The solution is simpler than most frameworks make it seem. Here's the approach that actually works:

1. **Break down** what you're actually building into fundamental components
2. **Solve each problem** with proper software engineering best practices
3. **ONLY INCLUDE AN LLM STEP** when it's impossible to solve with deterministic code

### The Golden Rule
**Making an LLM API call is the most expensive and most dangerous operation in modern software development.** While incredibly powerful, you want to avoid it at all costs and only use it when absolutely necessary.

### The Strategy
Break a big problem into small steps. Solve as many as possible with normal code (if/else, loops). Only use an LLM when "reasoning with context" is absolutely required.

**Most steps in your workflows should be regular code - not LLM calls.**

### Context Engineering: The Fundamental Skill

When you do make that LLM call, it's all about **context engineering**. To get a good answer back, you need:
- The **right context** at the **right time**
- Sent to the **right model**
- Pre-processed so the LLM can easily and reliably solve the problem

You need to pre-process all available information, prompts, and user input so the LLM can easily and reliably solve the problem. **This is the most fundamental skill in working with LLMs.**

### Why This Matters
- **Cost**: Each LLM API call costs money (often $0.01-$0.10 per request)
- **Speed**: LLM calls take 1-5 seconds, while normal code runs in milliseconds
- **Reliability**: LLMs are probabilistic—they might give different answers to the same question
- **Debugging**: Standard code is easier to debug than "black box" AI decisions
- **Danger**: LLM calls can produce unexpected outputs that break your system

---

## The 7 Foundational Building Blocks

These are the fundamental primitives. But how do you actually combine them? That's where **workflow orchestration** comes in - prompt chaining, routing, reflection, and other agentic patterns that emerge when you combine these building blocks strategically.

Given all of this, you only need these seven core building blocks to solve almost any business problem. Take your big problem, break it down into smaller problems, then solve each one using these building blocks chained together - that's how you build effective AI agents.

### Block 1: Intelligence 🧠
*The only truly "AI" component*

**What it is:** The actual API call to the Large Language Model (LLM). This is the only "AI" part of your stack.

**How it works:** You send text to an LLM, it thinks about it, and sends text back. That's it. Without this, you just have regular software. The tricky part isn't the LLM call itself - it's everything else you need to build around it.

**The Junior Mistake:** Treating the LLM as a wizard that knows everything.

**The Senior Reality:** The LLM is a text processing engine. It takes text in and predicts the next text out. It's expensive and slow compared to normal code. The real skill is **context engineering** - preparing the right context so the LLM can reliably solve your specific problem.

#### API Syntax: Traditional vs. New

OpenAI provides two API interfaces. Throughout this guide, we show both:

**Traditional API (`chat.completions.create`):**
- Uses `messages` array with role-based structure
- Supports system messages, user messages, assistant messages
- Returns `response.choices[0].message.content`
- More flexible for multi-turn conversations

**New API (`responses.create`):**
- Uses simple `input` string parameter
- Simpler syntax for single-turn interactions
- Returns `response.output_text`
- For multi-turn conversations, build conversation history as a string

**When to use which:**
- **New API**: Simple single-turn requests, when you want cleaner code
- **Traditional API**: Complex conversations with system prompts, tool calling, structured output with `response_format`

Both APIs work the same way - they're just different interfaces to the same underlying models. Choose based on your needs.

#### Real-World Example 1: Simple Chatbot

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# This is Block 1: The Intelligence Layer
# Using the traditional chat.completions API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)
# Output: "Hi there! How can I help you?"

# Using the new responses.create API (simpler syntax)
response_new = client.responses.create(
    model="gpt-4",
    input="Hello"
)

print(response_new.output_text)
# Output: "Hi there! How can I help you?"
```

**What happened:** You sent the string "Hello" to OpenAI's API and received "Hi there! How can I help you?" This is the raw engine that powers everything else. The new `responses.create()` API provides a simpler interface for single-turn conversations.

#### Real-World Example 2: Ticket Summarizer

**Scenario:** You're building a customer support system. A messy email comes in from a customer complaining about a broken toaster.

**Input:**
```
Subject: URGENT - My toaster is broken!!!
Body: Hi, I bought this toaster last week and it's not working. 
The bread just sits there and doesn't toast. I'm really frustrated 
because I need it for breakfast tomorrow. Can someone help me ASAP?
```

**Code:**
```python
def summarize_ticket(email_content):
    # Using the traditional chat.completions API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a ticket summarizer. Extract key information."},
            {"role": "user", "content": f"Summarize this ticket:\n\n{email_content}"}
        ]
    )
    return response.choices[0].message.content

# Using the new responses.create API
def summarize_ticket_new(email_content):
    # Combine system instruction and user input into a single input string
    input_text = f"You are a ticket summarizer. Extract key information.\n\nSummarize this ticket:\n\n{email_content}"
    response = client.responses.create(
        model="gpt-4",
        input=input_text
    )
    return response.output_text

summary = summarize_ticket(email_content)
# Output: "Customer reports broken toaster purchased last week. 
#          Bread doesn't toast. Urgent - needed for breakfast tomorrow."
```

**Why this matters:** Instead of a human reading a long email, the LLM extracts the key information in seconds.

#### Real-World Example 3: Context Engineering in Action

**Scenario:** You're building a code review assistant. The key to success is preparing the right context.

**Bad Context Engineering (Poor Results):**
```python
# Just dumping code without structure
code = read_file("app.py")
# Using traditional API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Review this code: {code}"}]
)
# ❌ LLM doesn't know what to focus on, might miss important issues

# Using new API
response_new = client.responses.create(
    model="gpt-4",
    input=f"Review this code: {code}"
)
# ❌ LLM doesn't know what to focus on, might miss important issues
```

**Good Context Engineering (Better Results):**
```python
def review_code(file_path: str, related_files: list[str] = None):
    """Review code with proper context engineering"""
    
    # Step 1: Pre-process the code
    code_content = read_file(file_path)
    file_extension = file_path.split('.')[-1]
    language = detect_language(file_extension)
    
    # Step 2: Gather related context
    context_parts = []
    
    # Add file metadata
    context_parts.append(f"File: {file_path}")
    context_parts.append(f"Language: {language}")
    
    # Add related files if provided
    if related_files:
        related_code = "\n".join([f"Related file {f}:\n{read_file(f)}" for f in related_files])
        context_parts.append(f"Related files:\n{related_code}")
    
    # Add code with clear structure
    context_parts.append(f"Code to review:\n```{language}\n{code_content}\n```")
    
    # Step 3: Prepare focused prompt
    system_prompt = """You are a senior code reviewer. Focus on:
    - Security vulnerabilities
    - Performance issues
    - Code quality and maintainability
    - Best practices for this language
    """
    
    user_prompt = "\n\n".join(context_parts)
    
    # Step 4: Send well-structured context
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Using new API - combine system prompt and user prompt
    combined_input = f"{system_prompt}\n\n{user_prompt}"
    response_new = client.responses.create(
        model="gpt-4",
        input=combined_input
    )
    
    return response.choices[0].message.content  # Traditional API
    # return response_new.output_text  # New API
# ✅ LLM has clear context, knows what to focus on, produces better reviews
```

**Key Context Engineering Principles:**
1. **Structure your input** - Use clear sections, formatting, and hierarchy
2. **Provide relevant context** - Include related files, metadata, and background
3. **Use system prompts** - Set clear expectations and role
4. **Pre-process data** - Clean, format, and organize before sending
5. **Right model for the task** - Use GPT-4 for complex reasoning, GPT-3.5 for simple tasks

#### Key Takeaways:
- This is the **only probabilistic** part of your system
- It's expensive: Each call costs money
- It's slow: Takes 1-5 seconds vs milliseconds for normal code
- Use it strategically, not for everything
- **Context engineering is the fundamental skill** - prepare context so the LLM can reliably solve your problem

---

### Block 2: Memory 🗃️
*Context persistence across interactions*

**What it is:** Context persistence. The ability to remember previous conversations.

**The Problem:** LLMs don't remember anything from previous messages. Without memory, each interaction starts from scratch because LLMs are stateless. If you ask an LLM "Tell me a joke" and then ask "What did I just ask?", it won't know because it doesn't remember previous interactions.

**The Junior Mistake:** Sending "What was my last question?" to the API and getting "I don't know" as a response.

**The Senior Reality:** You must manually pass in the conversation history each time. This is just storing and passing conversation state - something we've been doing in web apps forever. You manually manage the "Conversation History" list and send the entire relevant history back to the model with every new request.

#### Real-World Example 1: Chatbot with Memory

**Scenario:** Building a chatbot where the user can ask follow-up questions.

**Without Memory (Broken):**
```python
# First message
# Using traditional API
response1 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hi, my name is Dave."}]
)
# Response: "Hello Dave! Nice to meet you."

# Using new API
response1_new = client.responses.create(
    model="gpt-4",
    input="Hi, my name is Dave."
)
# Response: "Hello Dave! Nice to meet you."

# Second message - NO MEMORY
# Using traditional API
response2 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is my name?"}]
)
# Response: "I don't know your name. You haven't told me yet." ❌

# Using new API
response2_new = client.responses.create(
    model="gpt-4",
    input="What is my name?"
)
# Response: "I don't know your name. You haven't told me yet." ❌
```

**With Memory (Fixed):**
```python
# Store conversation history
messages = [
    {"role": "user", "content": "Hi, my name is Dave."}
]

# First message
# Using traditional API
response1 = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
# Response: "Hello Dave! Nice to meet you."

# Using new API - build conversation history as a single input
conversation_history = "User: Hi, my name is Dave.\n"
response1_new = client.responses.create(
    model="gpt-4",
    input=conversation_history
)
assistant_response1 = response1_new.output_text
# Response: "Hello Dave! Nice to meet you."

# Add assistant's response to history
messages.append({
    "role": "assistant", 
    "content": response1.choices[0].message.content
})

# For new API, append to conversation string
conversation_history += f"Assistant: {assistant_response1}\n"

# Add new user message
messages.append({
    "role": "user", 
    "content": "What is my name?"
})

conversation_history += "User: What is my name?\n"

# Second message - WITH MEMORY
# Using traditional API
response2 = client.chat.completions.create(
    model="gpt-4",
    messages=messages  # Sends entire history
)
# Response: "Your name is Dave!" ✅

# Using new API - send full conversation history
response2_new = client.responses.create(
    model="gpt-4",
    input=conversation_history
)
# Response: "Your name is Dave!" ✅
```

#### Real-World Example 2: Coding Assistant

**Scenario:** A developer is debugging code with your assistant.

```python
conversation_history = []

def chat_with_assistant(user_message):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Send entire history to LLM
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history
    )
    
    assistant_message = response.choices[0].message.content
    
    # Add assistant response to history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# User: "My code is broken."
chat_with_assistant("My code is broken.")
# Response: "I'd be happy to help! Can you share the error message?"

# User: "Here is the error message."
chat_with_assistant("Here is the error message: TypeError: cannot read property 'name' of undefined")
# Response: "Based on the error, it seems like you're trying to access 
#           the 'name' property of something that's undefined. Can you 
#           share the code where this error occurs?"
```

**Why this matters:** Without memory, every message is treated as a brand-new conversation. The assistant can't understand context or follow-up questions.

#### Real-World Example 3: Customer Support Bot

**Scenario:** A customer is having a multi-step conversation about their order.

```python
class CustomerSupportBot:
    def __init__(self):
        self.conversations = {}  # Store by customer_id
    
    def handle_message(self, customer_id, message):
        # Get or create conversation history for this customer
        if customer_id not in self.conversations:
            self.conversations[customer_id] = []
            self.conversations_text = {}  # For new API
        
        history = self.conversations[customer_id]
        
        # Add user message
        history.append({"role": "user", "content": message})
        
        # Get response with full context
        # Using traditional API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=history
        )
        
        # Using new API - build conversation string
        if customer_id not in self.conversations_text:
            self.conversations_text[customer_id] = ""
        self.conversations_text[customer_id] += f"User: {message}\n"
        
        response_new = client.responses.create(
            model="gpt-4",
            input=self.conversations_text[customer_id]
        )
        
        assistant_message = response.choices[0].message.content
        assistant_message_new = response_new.output_text
        history.append({"role": "assistant", "content": assistant_message})
        self.conversations_text[customer_id] += f"Assistant: {assistant_message_new}\n"
        
        return assistant_message  # or assistant_message_new for new API

bot = CustomerSupportBot()

# Customer 1: "Where is my order?"
bot.handle_message("customer_123", "Where is my order?")
# Response: "I'd be happy to help! Can you provide your order number?"

# Customer 1: "It's #45678"
bot.handle_message("customer_123", "It's #45678")
# Response: "Order #45678 is currently being prepared and will ship tomorrow."
# ✅ The bot remembers this is about order #45678

# Customer 2: "Where is my order?"
bot.handle_message("customer_789", "Where is my order?")
# Response: "I'd be happy to help! Can you provide your order number?"
# ✅ Different conversation history for different customer
```

#### Key Takeaways:
- LLMs are **stateless** - they forget everything after each call
- You must **manually store** conversation history
- Send the **entire relevant history** with each request
- Consider **token limits** - very long histories get expensive and may exceed limits
- Use **conversation IDs** to manage multiple users

---

### Block 3: Tools 🛠️
*External system integration capabilities*

**What it is:** Giving the LLM the ability to "do" things, not just talk. This is also called "Function Calling" or "Tool Use."

**The Problem:** Most of the time you need your LLM to actually do stuff, not just chat. Pure text generation is limited - you want to call APIs, update databases, or read files. LLMs are trapped in a text box. They cannot access the internet, check the time, query a database, or perform actions unless you give them Tools.

**The Junior Mistake:** Asking the LLM "What is the weather in Tokyo?" and getting a hallucination or "I don't know, my data cut off in 2023."

**The Senior Reality:** Tools let the LLM say "I need to call this function with these parameters" and your code handles the actual execution. This is just normal API integration where the LLM picks what to call and provides JSON input for the arguments. You define a function (e.g., `get_weather(city)`). You describe this function to the LLM. The LLM decides if it needs to call it based on the user's prompt. **Important:** The LLM does NOT execute the code. It returns a specific text output saying "I want to run get_weather for 'Tokyo'". YOUR CODE spots this, runs the function, and feeds the result back to the LLM.

#### Real-World Example 1: Weather Bot

**Scenario:** User asks "What's the weather in London?"

**Step 1: Define the Tool**
```python
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # This is YOUR code - it calls a real weather API
    import requests
    api_key = "your-weather-api-key"
    url = f"https://api.weather.com/v1/current?city={city}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return f"Temperature: {data['temp']}°C, Condition: {data['condition']}"
```

**Step 2: Describe the Tool to the LLM**
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

**Step 3: Let LLM Decide to Use the Tool**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in London?"}],
    tools=tools,
    tool_choice="auto"  # Let the model decide
)

# The LLM responds with a "tool call" request
message = response.choices[0].message

if message.tool_calls:
    # LLM wants to call a tool
    tool_call = message.tool_calls[0]
    
    if tool_call.function.name == "get_weather":
        # Extract the argument
        import json
        arguments = json.loads(tool_call.function.arguments)
        city = arguments["city"]  # "London"
        
        # YOUR CODE runs the function
        weather_result = get_weather(city)
        # Result: "Temperature: 15°C, Condition: Rainy"
        
        # Send the result back to the LLM
        messages.append(message)  # Add the tool call request
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": weather_result
        })
        
        # Get final response
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        print(final_response.choices[0].message.content)
        # Output: "It is currently raining in London with a temperature of 15°C."
```

#### Real-World Example 2: E-commerce Order Tracker

**Scenario:** User asks "Where is my order #123?"

```python
def check_order_status(order_id: str) -> dict:
    """Check the status of an order in the database."""
    # This queries YOUR database
    import sqlite3
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {"status": result[0], "order_id": order_id}
    else:
        return {"status": "not_found", "order_id": order_id}

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Check the shipping status of an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to check"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]

# User asks about order
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Where is my order #123?"}],
    tools=tools
)

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    
    if tool_call.function.name == "check_order_status":
        arguments = json.loads(tool_call.function.arguments)
        order_id = arguments["order_id"]  # "123"
        
        # YOUR CODE runs the database query
        order_data = check_order_status(order_id)
        # Result: {"status": "shipped", "order_id": "123"}
        
        # Send result back to LLM
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(order_data)
        })
        
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        print(final_response.choices[0].message.content)
        # Output: "Your order #123 has been shipped! It should arrive within 3-5 business days."
```

#### Real-World Example 3: Calendar Assistant

**Scenario:** User wants to schedule a meeting.

```python
def create_calendar_event(title: str, date: str, time: str) -> dict:
    """Create a calendar event."""
    # This integrates with YOUR calendar API (Google Calendar, Outlook, etc.)
    event = {
        "title": title,
        "date": date,
        "time": time,
        "created": True
    }
    # Actually create the event via API
    # calendar_api.create_event(event)
    return event

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a new calendar event",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string", "format": "YYYY-MM-DD"},
                    "time": {"type": "string", "format": "HH:MM"}
                },
                "required": ["title", "date", "time"]
            }
        }
    }
]

# User: "Schedule a team meeting for next Monday at 2pm"
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Schedule a team meeting for next Monday at 2pm"}],
    tools=tools
)

# LLM decides to call create_calendar_event with:
# title: "Team Meeting"
# date: "2024-01-15" (next Monday)
# time: "14:00"

# YOUR CODE creates the actual calendar event
# LLM formats the confirmation message
```

#### Key Takeaways:
- LLMs **cannot execute code** - they only request tool calls
- **Your code** executes the tools and returns results
- Tools let LLMs interact with **real systems** (databases, APIs, services)
- Always **validate** tool inputs before executing
- Consider **security** - don't let LLMs call dangerous functions without safeguards

---

### Block 4: Validation ✅
*Quality assurance and structured data enforcement*

**What it is:** Enforcing a specific data shape (JSON) instead of raw text. This is arguably the most important block for production.

**The Problem:** You need to make sure the LLM returns JSON that matches your expected schema. LLMs are probabilistic. If you ask for a list of tasks, one time it might give you bullet points, the next time a paragraph. You cannot code against that.

**The Junior Mistake:** Parsing raw string output with Regex, hoping the LLM formatted the date correctly.

**The Senior Reality:** You validate the JSON output against a predefined structure. If validation fails, you can send it back to the LLM to fix it. This ensures downstream code can reliably work with the data. This is just normal schema validation with retry logic using tools like Pydantic, Zod, or data classes. Using schema enforcement (like Pydantic in Python or Zod in TypeScript) to force the LLM to return valid JSON. If the validation fails, you automatically send the error back to the LLM to fix it.

#### Real-World Example 1: Task Extractor

**Scenario:** You're building a Project Manager bot. User inputs: "I need to finish the slide deck by Friday, it's super urgent."

**Without Validation (Broken):**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "I need to finish the slide deck by Friday, it's super urgent."}]
)

output = response.choices[0].message.content
# Output might be:
# "Task: Finish slide deck
#  Due: Friday
#  Priority: High"
# OR
# "You have a task: finish the slide deck. It's due Friday and is urgent."
# OR
# "• Task: Finish slide deck
#  • Due date: Friday  
#  • Priority: Urgent"

# Now you have to parse this with regex - nightmare! ❌
```

**With Validation (Fixed):**
```python
from pydantic import BaseModel
from typing import Literal

class Task(BaseModel):
    task: str
    due_date: str
    priority: Literal["Low", "Medium", "High"]

# Define the response format
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "task_extractor",
        "schema": Task.model_json_schema(),
        "strict": True
    }
}

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "I need to finish the slide deck by Friday, it's super urgent."}],
    response_format=response_format
)

# Parse the JSON response
import json
task_data = json.loads(response.choices[0].message.content)
task = Task(**task_data)

print(task.task)      # "Finish slide deck"
print(task.due_date)  # "Friday"
print(task.priority)  # "High"

# Now you can reliably save this to your database! ✅
```

#### Real-World Example 2: Invoice Extraction System

**Scenario:** You're processing invoices from PDFs. You need the total amount as a float, not a string like "about $50".

**Without Validation:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Extract invoice data from: {pdf_text}"}]
)

output = response.choices[0].message.content
# Might be: "Total: about $50.00"
# Or: "Total amount: 50 dollars"
# Or: "The invoice total is approximately $50"

# How do you extract $50.00 reliably? Regex nightmare! ❌
```

**With Validation:**
```python
from pydantic import BaseModel, Field
from decimal import Decimal

class Invoice(BaseModel):
    invoice_number: str
    date: str
    total: Decimal = Field(description="Total amount as a decimal number")
    vendor: str
    items: list[dict]

response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "invoice_extractor",
        "schema": Invoice.model_json_schema(),
        "strict": True
    }
}

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Extract invoice data: {pdf_text}"}],
    response_format=response_format
)

invoice_data = json.loads(response.choices[0].message.content)
invoice = Invoice(**invoice_data)

print(invoice.total)  # Decimal('50.00') - guaranteed to be a number! ✅
print(type(invoice.total))  # <class 'decimal.Decimal'>

# Now you can do math with it, store it in database, etc.
```

#### Real-World Example 3: Email Classifier with Retry Logic

**Scenario:** Classifying customer emails into categories with automatic retry on validation failure.

```python
from pydantic import BaseModel, ValidationError
from typing import Literal

class EmailClassification(BaseModel):
    category: Literal["Question", "Complaint", "Request", "Feedback"]
    urgency: Literal["Low", "Medium", "High"]
    sentiment: Literal["Positive", "Neutral", "Negative"]
    summary: str

def classify_email(email_content: str, max_retries: int = 3) -> EmailClassification:
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "email_classifier",
            "schema": EmailClassification.model_json_schema(),
            "strict": True
        }
    }
    
    messages = [
        {"role": "system", "content": "Classify this email into the specified categories."},
        {"role": "user", "content": email_content}
    ]
    
    for attempt in range(max_retries):
        try:
            # Using traditional API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                response_format=response_format
            )
            
            # Using new API - combine system and user messages
            input_text = f"Classify this email into the specified categories.\n\n{email_content}"
            # Note: New API may handle response_format differently - check API docs
            response_new = client.responses.create(
                model="gpt-4",
                input=input_text
            )
            
            # Try to parse and validate
            data = json.loads(response.choices[0].message.content)
            # For new API: data = json.loads(response_new.output_text)
            classification = EmailClassification(**data)
            return classification  # Success!
            
        except (json.JSONDecodeError, ValidationError) as e:
            # Validation failed - send error back to LLM
            if attempt < max_retries - 1:
                messages.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                messages.append({
                    "role": "user",
                    "content": f"Validation error: {str(e)}. Please fix the JSON format."
                })
                # For new API, rebuild input with error message
                input_text = f"{input_text}\n\nError: {str(e)}. Please provide valid JSON."
            else:
                # Max retries reached - return default
                return EmailClassification(
                    category="Question",
                    urgency="Medium",
                    sentiment="Neutral",
                    summary="Unable to classify"
                )
    
    return None

# Usage
email = "I'm really frustrated! My order hasn't arrived and it's been 2 weeks!"
classification = classify_email(email)

print(classification.category)   # "Complaint"
print(classification.urgency)  # "High"
print(classification.sentiment) # "Negative"
```

#### Real-World Example 4: Form Data Extractor

**Scenario:** Extracting structured data from unstructured text (like filling out a form).

```python
class ContactForm(BaseModel):
    name: str
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: str
    message: str
    preferred_contact_method: Literal["Email", "Phone"]

def extract_contact_info(text: str) -> ContactForm:
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "contact_extractor",
            "schema": ContactForm.model_json_schema(),
            "strict": True
        }
    }
    
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Extract contact information from: {text}"
        }],
        response_format=response_format
    )
    
    # Using new API
    response_new = client.responses.create(
        model="gpt-4",
        input=f"Extract contact information from: {text}. Return as JSON matching this schema: {ContactForm.model_json_schema()}"
    )
    
    data = json.loads(response.choices[0].message.content)
    # For new API: data = json.loads(response_new.output_text)
    return ContactForm(**data)

# Input: Unstructured text
text = """
Hi, I'm John Smith. You can reach me at john@example.com or call me at 555-1234.
I'd prefer email. My message is: I'm interested in your product.
"""

contact = extract_contact_info(text)
print(contact.name)  # "John Smith"
print(contact.email)  # "john@example.com"
print(contact.phone)  # "555-1234"
print(contact.preferred_contact_method)  # "Email"
```

#### Key Takeaways:
- LLMs are **probabilistic** - same input can give different formats
- **Structured output** guarantees consistent data shapes
- Use **schema validation** (Pydantic, Zod) to enforce types
- **Retry logic** can fix validation errors automatically
- This is **critical for production** - you can't build reliable systems on unpredictable text

---

### Block 5: Control 🚦
*Deterministic decision-making and process flow*

**What it is:** Using the LLM to classify intent, then using standard code to direct the workflow.

**The Junior Mistake:** Letting a "General Agent" loop endlessly trying to figure out what to do.

**The Senior Reality:** You don't want your LLM making every decision - some things should be handled by regular code. Use if/else statements, switch cases, and routing logic to direct flow based on conditions. This is just normal business logic and routing that you'd write in any application. Instead, ask it to **Classify** the input, then use **if/else statements** in your code to route the user.

**Why not use Tools for this?** Using a classification step creates a log of reasoning (why did it think this was a complaint?), which is easier to debug than a black-box tool call.

#### Real-World Example 1: Customer Service Router

**Scenario:** A customer support email comes in. You need to route it to the right team.

**Without Control (Inefficient):**
```python
# Bad: Letting LLM decide everything
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": customer_email}],
    tools=[refund_tool, tech_support_tool, feature_request_tool]
)
# LLM might call wrong tool, or call multiple tools, or loop forever ❌
```

**With Control (Efficient):**
```python
from pydantic import BaseModel
from typing import Literal

class IntentClassification(BaseModel):
    intent: Literal["Question", "Complaint", "Request", "Feedback"]
    confidence: float
    reasoning: str

def classify_intent(email: str) -> IntentClassification:
    """Step 1: Classify the intent"""
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "intent_classifier",
            "schema": IntentClassification.model_json_schema(),
            "strict": True
        }
    }
    
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Classify this customer email: {email}"
        }],
        response_format=response_format
    )
    
    # Using new API
    input_text = f"Classify this customer email into one of these categories: Question, Complaint, Request, Feedback. Return JSON with intent, confidence, and reasoning.\n\nEmail: {email}"
    response_new = client.responses.create(
        model="gpt-4",
        input=input_text
    )
    
    data = json.loads(response.choices[0].message.content)
    # For new API: data = json.loads(response_new.output_text)
    return IntentClassification(**data)

def route_email(email: str):
    """Step 2: Route based on classification"""
    classification = classify_intent(email)
    
    # Deterministic routing logic
    if classification.intent == "Question":
        route_to_qa_bot(email)
    elif classification.intent == "Complaint":
        route_to_human_escalation(email, priority="High")
    elif classification.intent == "Request":
        route_to_feature_tracking(email)
    elif classification.intent == "Feedback":
        route_to_feedback_system(email)
    
    # Log the reasoning for debugging
    log_classification(email, classification.reasoning)

# Usage
customer_email = "I want a refund for my order #12345"
route_email(customer_email)
# 1. LLM classifies: intent="Request", reasoning="Customer wants refund"
# 2. Code routes to: route_to_feature_tracking()
# 3. Logged for debugging ✅
```

#### Real-World Example 2: Multi-Step Workflow Router

**Scenario:** Building a travel booking assistant that handles different types of requests.

```python
class TravelIntent(BaseModel):
    action: Literal["BookFlight", "BookHotel", "CancelBooking", "CheckStatus", "GetRecommendations"]
    entities: dict  # Extracted entities like dates, locations

def route_travel_request(user_message: str):
    """Classify then route"""
    # Step 1: Classify
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "travel_intent",
            "schema": TravelIntent.model_json_schema(),
            "strict": True
        }
    }
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        response_format=response_format
    )
    
    intent = TravelIntent(**json.loads(response.choices[0].message.content))
    
    # Step 2: Route with deterministic code
    if intent.action == "BookFlight":
        return handle_flight_booking(intent.entities)
    elif intent.action == "BookHotel":
        return handle_hotel_booking(intent.entities)
    elif intent.action == "CancelBooking":
        return handle_cancellation(intent.entities)
    elif intent.action == "CheckStatus":
        return check_booking_status(intent.entities)
    elif intent.action == "GetRecommendations":
        return get_travel_recommendations(intent.entities)

def handle_flight_booking(entities: dict):
    """Deterministic flight booking logic"""
    origin = entities.get("origin")
    destination = entities.get("destination")
    date = entities.get("date")
    
    # Use tools to search flights
    flights = search_flights(origin, destination, date)
    
    # Use LLM to format response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Present these flight options: {flights}"
        }]
    )
    return response.choices[0].message.content

# Usage
user_message = "I need to book a flight from New York to London on March 15th"
result = route_travel_request(user_message)
```

#### Real-World Example 3: Content Moderation System

**Scenario:** Classifying user-generated content to determine if it needs moderation.

```python
class ContentClassification(BaseModel):
    category: Literal["Safe", "Spam", "Inappropriate", "Copyright", "NeedsReview"]
    severity: Literal["Low", "Medium", "High"]
    flagged_keywords: list[str]

def moderate_content(content: str) -> dict:
    """Classify content, then take action"""
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "content_classifier",
            "schema": ContentClassification.model_json_schema(),
            "strict": True
        }
    }
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Classify this content for moderation: {content}"
        }],
        response_format=response_format
    )
    
    classification = ContentClassification(**json.loads(response.choices[0].message.content))
    
    # Deterministic action based on classification
    if classification.category == "Safe":
        return {"action": "approve", "content": content}
    elif classification.category == "Spam":
        return {"action": "delete", "reason": "Spam detected"}
    elif classification.category == "Inappropriate":
        if classification.severity == "High":
            return {"action": "delete_and_ban", "reason": "Severe violation"}
        else:
            return {"action": "flag_for_review", "reason": "Inappropriate content"}
    elif classification.category == "Copyright":
        return {"action": "flag_for_legal_review", "reason": "Possible copyright violation"}
    elif classification.category == "NeedsReview":
        return {"action": "queue_for_human_review", "reason": "Uncertain classification"}
```

#### Real-World Example 4: Smart FAQ System

**Scenario:** Routing questions to the right knowledge base or human expert.

```python
class QuestionClassification(BaseModel):
    topic: Literal["Billing", "Technical", "Account", "Product", "Other"]
    can_answer_with_faq: bool
    suggested_faq_id: str | None
    needs_human: bool

def handle_customer_question(question: str):
    """Classify question, then route to appropriate resource"""
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "question_classifier",
            "schema": QuestionClassification.model_json_schema(),
            "strict": True
        }
    }
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        response_format=response_format
    )
    
    classification = QuestionClassification(**json.loads(response.choices[0].message.content))
    
    # Route based on classification
    if classification.can_answer_with_faq and classification.suggested_faq_id:
        # Use deterministic code to fetch FAQ
        faq = get_faq_by_id(classification.suggested_faq_id)
        return format_faq_response(faq)
    elif classification.needs_human:
        # Route to human expert based on topic
        if classification.topic == "Billing":
            return route_to_billing_team(question)
        elif classification.topic == "Technical":
            return route_to_tech_support(question)
        else:
            return route_to_general_support(question)
    else:
        # Try to answer with LLM + knowledge base
        return answer_with_knowledge_base(question, classification.topic)
```

#### Key Takeaways:
- Don't let LLM make **every decision** - it's slow and expensive
- Use LLM to **classify** intent, then use **if/else** for routing
- This creates **audit trails** - you can see why decisions were made
- **Easier to debug** than black-box agent decisions
- **Faster** - classification is one LLM call, not multiple tool calls

---

### Block 6: Recovery 🛟
*Graceful failure management*

**What it is:** Error handling for AI. The safety net when things go wrong.

**The Reality:** Things will go wrong - APIs will be down, LLMs will return nonsense, rate limits will hit you. APIs go down. LLMs hallucinate. Rate limits hit. Networks fail. Models output garbage.

**The Junior Mistake:** The script crashes with an Unhandled Exception and the user sees a 500 Error.

**The Senior Reality:** You need try/catch blocks, retry logic with backoff, and fallback responses when stuff breaks. This is just standard error handling that you'd implement in any production system. You assume failure. You implement Retries, Backoffs, and Fallbacks.

#### Real-World Example 1: Retry with Exponential Backoff

**Scenario:** Handling transient API failures.

```python
import time
import random
from openai import OpenAI, APIError, RateLimitError

def call_llm_with_retry(messages=None, input_text=None, max_retries=3, base_delay=1):
    """Call LLM with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            # Using traditional API
            if messages:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                return response.choices[0].message.content
            
            # Using new API
            if input_text:
                response = client.responses.create(
                    model="gpt-4",
                    input=input_text
                )
                return response.output_text
            
        except RateLimitError as e:
            # Rate limit hit - wait longer
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit hit. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                return fallback_response("Rate limit exceeded. Please try again later.")
                
        except APIError as e:
            # Other API errors
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"API error: {e}. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                return fallback_response("Service temporarily unavailable. Please try again later.")
                
        except Exception as e:
            # Unexpected errors
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Unexpected error: {e}. Retrying...")
                time.sleep(delay)
            else:
                return fallback_response("An error occurred. Please contact support.")

def fallback_response(reason: str) -> str:
    """Hardcoded fallback when all retries fail"""
    return f"I'm sorry, I'm having trouble right now. {reason}"

# Usage
messages = [{"role": "user", "content": "Hello"}]
response = call_llm_with_retry(messages)
```

#### Real-World Example 2: Travel Booking Bot with Recovery

**Scenario:** The user asks for a flight. The LLM generates invalid JSON for the flight date.

```python
from pydantic import BaseModel, ValidationError
from datetime import datetime

class FlightRequest(BaseModel):
    origin: str
    destination: str
    date: datetime
    passengers: int

def book_flight_with_recovery(user_message: str):
    """Book flight with multiple recovery strategies"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Try to extract flight details
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "flight_request",
                    "schema": FlightRequest.model_json_schema(),
                    "strict": True
                }
            }
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
                response_format=response_format
            )
            
            # Try to parse and validate
            data = json.loads(response.choices[0].message.content)
            flight_request = FlightRequest(**data)
            
            # Success! Search for flights
            flights = search_flights(
                flight_request.origin,
                flight_request.destination,
                flight_request.date
            )
            return format_flight_results(flights)
            
        except json.JSONDecodeError as e:
            # Recovery 1: Invalid JSON - ask LLM to fix it
            if attempt < max_retries - 1:
                messages.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                messages.append({
                    "role": "user",
                    "content": f"The JSON was invalid: {str(e)}. Please provide valid JSON."
                })
                continue
            else:
                # Recovery 2: Fallback to human
                return "I'm having trouble understanding your flight request. Please contact our booking team at 1-800-FLIGHTS."
                
        except ValidationError as e:
            # Recovery 3: Validation failed - ask for clarification
            if attempt < max_retries - 1:
                error_fields = [err['loc'][0] for err in e.errors()]
                messages.append({
                    "role": "user",
                    "content": f"Please provide: {', '.join(error_fields)}"
                })
                continue
            else:
                return "I need more information to book your flight. Please specify origin, destination, and date."
                
        except Exception as e:
            # Recovery 4: Unexpected error - fallback
            log_error(e)
            return "I'm experiencing technical difficulties. Please try again or contact support."

# Usage
user_message = "I want to fly from New York to London"
result = book_flight_with_recovery(user_message)
```

#### Real-World Example 3: Knowledge Base Retrieval with Fallback

**Scenario:** Your bot tries to answer a question using a Knowledge Base. The retrieval fails.

```python
def answer_question_with_fallback(question: str):
    """Answer question with multiple fallback strategies"""
    try:
        # Strategy 1: Try knowledge base retrieval
        relevant_docs = retrieve_from_knowledge_base(question)
        
        if relevant_docs:
            # Use LLM to answer based on docs
            # Using traditional API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Answer based on the provided documentation."},
                    {"role": "user", "content": f"Docs: {relevant_docs}\n\nQuestion: {question}"}
                ]
            )
            # Using new API
            input_text = f"Answer based on the provided documentation.\n\nDocs: {relevant_docs}\n\nQuestion: {question}"
            response_new = client.responses.create(
                model="gpt-4",
                input=input_text
            )
            return response.choices[0].message.content  # or response_new.output_text
            
    except KnowledgeBaseError as e:
        # Recovery 1: Knowledge base failed - try general LLM answer
        try:
            # Using traditional API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            # Using new API
            response_new = client.responses.create(
                model="gpt-4",
                input=question
            )
            return f"{response.choices[0].message.content}\n\n(Note: I couldn't access our knowledge base, so this is a general answer.)"
            
        except Exception as e2:
            # Recovery 2: LLM also failed - hardcoded fallback
            return "I'm sorry, I couldn't access the manual right now. Please try again later or contact support."
    
    except Exception as e:
        # Recovery 3: Unexpected error
        log_error(e)
        return "I'm experiencing technical difficulties. Please try again later."

def retrieve_from_knowledge_base(question: str):
    """Simulate knowledge base retrieval"""
    # This might fail due to:
    # - Database connection error
    # - Search service down
    # - Network timeout
    # - Invalid query
    raise KnowledgeBaseError("Knowledge base unavailable")
```

#### Real-World Example 4: Multi-Layer Recovery Strategy

**Scenario:** Comprehensive error handling for a production AI system.

```python
class RecoveryStrategy:
    """Multi-layer recovery for AI operations"""
    
    def __init__(self):
        self.retry_count = 0
        self.max_retries = 3
    
    def execute_with_recovery(self, operation, fallback=None):
        """Execute operation with full recovery chain"""
        # Layer 1: Retry with exponential backoff
        for attempt in range(self.max_retries):
            try:
                return operation()
            except RateLimitError:
                if attempt < self.max_retries - 1:
                    self._exponential_backoff(attempt)
                    continue
                else:
                    return self._handle_rate_limit()
            except APIError as e:
                if attempt < self.max_retries - 1:
                    self._exponential_backoff(attempt)
                    continue
                else:
                    return self._handle_api_error(e)
            except ValidationError as e:
                return self._handle_validation_error(e, operation)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    self._exponential_backoff(attempt)
                    continue
                else:
                    return self._handle_unexpected_error(e, fallback)
        
        # Layer 2: Fallback function
        if fallback:
            return fallback()
        
        # Layer 3: Hardcoded response
        return self._hardcoded_fallback()
    
    def _exponential_backoff(self, attempt):
        delay = (2 ** attempt) + random.uniform(0, 1)
        time.sleep(delay)
    
    def _handle_rate_limit(self):
        return "I'm receiving too many requests. Please wait a moment and try again."
    
    def _handle_api_error(self, error):
        log_error(error)
        return "The AI service is temporarily unavailable. Please try again later."
    
    def _handle_validation_error(self, error, operation):
        # Try to fix validation error
        if hasattr(operation, 'fix_validation'):
            return operation.fix_validation(error)
        return "I had trouble understanding that. Could you rephrase?"
    
    def _handle_unexpected_error(self, error, fallback):
        log_error(error)
        if fallback:
            return fallback()
        return "An unexpected error occurred. Please contact support."
    
    def _hardcoded_fallback(self):
        return "I'm having technical difficulties. Our team has been notified."

# Usage
recovery = RecoveryStrategy()

def ai_operation():
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    return response.choices[0].message.content

def ai_operation_new():
    # Using new API
    response = client.responses.create(
        model="gpt-4",
        input="Hello"
    )
    return response.output_text

def fallback_operation():
    return "Hello! How can I help you today?"  # Simple fallback

result = recovery.execute_with_recovery(ai_operation, fallback_operation)
# or: result = recovery.execute_with_recovery(ai_operation_new, fallback_operation)
```

#### Key Takeaways:
- **Assume failure** - APIs will fail, networks will timeout
- Implement **retry logic** with exponential backoff
- Have **fallback responses** ready
- **Log errors** for debugging
- **Graceful degradation** - partial functionality is better than crashing
- **User-friendly messages** - don't show technical errors to users

---

### Block 7: Feedback 🛑
*Human oversight and approval workflows*

**What it is:** A "Full Stop" mechanism for sensitive actions. A safety valve for high-stakes operations.

**When to use it:** Sometimes you need a human to check the LLM's work before it goes live. Some decisions are too important or complex for full automation - like sending emails to customers or making purchases. For high-stakes actions like sending emails, making purchases, deleting data, posting to social media, or making financial transactions.

**The Junior Mistake:** Letting the AI send emails or post Tweets automatically without human oversight.

**The Senior Reality:** Add approval steps where humans can review and approve/reject before execution. This is just basic approval workflows like you'd build for any app. The AI prepares the draft, but the system pauses execution until a human clicks "Approve."

#### Real-World Example 1: Email Drafting with Approval

**Scenario:** An agent drafts a response to an angry client. Before sending, the workflow pauses for human approval.

```python
class EmailDraft:
    def __init__(self, to: str, subject: str, body: str):
        self.to = to
        self.subject = subject
        self.body = body
        self.status = "pending_approval"

def draft_client_response(client_email: str) -> EmailDraft:
    """Draft email response, but don't send it"""
    # Use LLM to draft response
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Draft a professional, empathetic response to this client email."},
            {"role": "user", "content": f"Client email: {client_email}"}
        ]
    )
    
    # Using new API
    input_text = f"Draft a professional, empathetic response to this client email.\n\nClient email: {client_email}"
    response_new = client.responses.create(
        model="gpt-4",
        input=input_text
    )
    
    draft_body = response.choices[0].message.content  # or response_new.output_text
    
    # Extract subject (or generate it)
    # Using traditional API
    subject_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate email subject for: {draft_body}"}]
    )
    # Using new API
    subject_response_new = client.responses.create(
        model="gpt-4",
        input=f"Generate email subject for: {draft_body}"
    )
    subject = subject_response.choices[0].message.content  # or subject_response_new.output_text
    
    # Create draft (NOT SENT YET)
    draft = EmailDraft(
        to=extract_email(client_email),
        subject=subject,
        body=draft_body
    )
    
    # Send notification to human for approval
    send_approval_notification(draft)
    
    return draft

def send_approval_notification(draft: EmailDraft):
    """Notify human manager via Slack/dashboard"""
    notification = {
        "type": "email_approval_required",
        "draft_id": draft.id,
        "to": draft.to,
        "subject": draft.subject,
        "body": draft.body,
        "actions": ["approve", "reject", "edit"]
    }
    
    # Send to Slack
    send_slack_message(
        channel="#customer-support",
        message=f"📧 Email draft ready for approval:\nTo: {draft.to}\nSubject: {draft.subject}\n\n{draft.body}\n\n[Approve] [Reject] [Edit]"
    )
    
    # Or send to dashboard
    save_to_approval_queue(notification)

def handle_approval(draft_id: str, action: str, edited_body: str = None):
    """Human reviews and approves/rejects"""
    draft = get_draft(draft_id)
    
    if action == "approve":
        # Human approved - NOW send the email
        send_email(draft.to, draft.subject, draft.body)
        draft.status = "sent"
        log_action("email_sent", draft_id)
        
    elif action == "reject":
        # Human rejected - don't send
        draft.status = "rejected"
        log_action("email_rejected", draft_id)
        
    elif action == "edit":
        # Human edited - use edited version
        draft.body = edited_body
        send_email(draft.to, draft.subject, edited_body)
        draft.status = "sent_edited"
        log_action("email_sent_edited", draft_id)

# Usage
client_email = "I'm very upset! My order is late and no one responded!"
draft = draft_client_response(client_email)
# System pauses here - waits for human approval
# Human clicks "Approve" -> Email is sent
# Human clicks "Reject" -> Email is discarded
# Human clicks "Edit" -> Human edits, then approves -> Edited email is sent
```

#### Real-World Example 2: Social Media Manager Bot

**Scenario:** AI reads industry news and drafts a LinkedIn post, but requires human approval before posting.

```python
class SocialMediaPost:
    def __init__(self, platform: str, content: str, scheduled_time: str = None):
        self.platform = platform
        self.content = content
        self.scheduled_time = scheduled_time
        self.status = "pending_approval"

def draft_social_media_post(industry_news: str) -> SocialMediaPost:
    """Draft social media post from industry news"""
    # Using traditional API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Create an engaging LinkedIn post about this industry news. Keep it professional and insightful."},
            {"role": "user", "content": industry_news}
        ]
    )
    
    # Using new API
    input_text = f"Create an engaging LinkedIn post about this industry news. Keep it professional and insightful.\n\n{industry_news}"
    response_new = client.responses.create(
        model="gpt-4",
        input=input_text
    )
    
    post_content = response.choices[0].message.content  # or response_new.output_text
    
    post = SocialMediaPost(
        platform="linkedin",
        content=post_content
    )
    
    # Require approval before posting
    request_approval(post)
    
    return post

def request_approval(post: SocialMediaPost):
    """Send notification to user for approval"""
    send_notification(
        user_id="user_123",
        message=f"📱 Proposed LinkedIn Post:\n\n{post.content}\n\n[Approve] [Reject] [Edit]",
        callback_url=f"/api/posts/{post.id}/approve"
    )
    
    # Store in pending queue
    save_to_pending_queue(post)

def handle_post_approval(post_id: str, action: str, edited_content: str = None):
    """Handle human approval/rejection"""
    post = get_post(post_id)
    
    if action == "approve":
        # Human approved - post to LinkedIn
        post_to_linkedin(post.content)
        post.status = "posted"
        
    elif action == "reject":
        # Human rejected - discard
        post.status = "rejected"
        
    elif action == "edit":
        # Human edited - post edited version
        post.content = edited_content
        post_to_linkedin(edited_content)
        post.status = "posted_edited"

# Usage
news = "AI technology advances in healthcare..."
post = draft_social_media_post(news)
# System waits for human approval
# Human reviews, approves/rejects/edits
```

#### Real-World Example 3: Financial Transaction Approval

**Scenario:** An AI assistant helps with expense reports, but requires approval before processing payments.

```python
class ExpenseRequest:
    def __init__(self, amount: float, vendor: str, description: str, category: str):
        self.amount = amount
        self.vendor = vendor
        self.description = description
        self.category = category
        self.status = "pending_approval"

def process_expense_receipt(receipt_image: str) -> ExpenseRequest:
    """Extract expense data from receipt, but don't process payment"""
    # Use vision model to extract data
    response = client.chat.completions.create(
        model="gpt-4-vision",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract expense information from this receipt."},
                {"type": "image_url", "image_url": receipt_image}
            ]
        }]
    )
    
    # Parse extracted data (using Block 4: Validation)
    expense_data = parse_expense_data(response.choices[0].message.content)
    
    expense = ExpenseRequest(
        amount=expense_data["amount"],
        vendor=expense_data["vendor"],
        description=expense_data["description"],
        category=expense_data["category"]
    )
    
    # Require manager approval for expenses over $100
    if expense.amount > 100:
        request_manager_approval(expense)
    else:
        # Auto-approve small expenses
        process_payment(expense)
    
    return expense

def request_manager_approval(expense: ExpenseRequest):
    """Send approval request to manager"""
    send_notification(
        manager_id=expense.manager_id,
        message=f"💰 Expense Approval Required:\nAmount: ${expense.amount}\nVendor: {expense.vendor}\nDescription: {expense.description}\n\n[Approve] [Reject]",
        callback_url=f"/api/expenses/{expense.id}/approve"
    )

def handle_expense_approval(expense_id: str, action: str):
    """Handle manager approval"""
    expense = get_expense(expense_id)
    
    if action == "approve":
        # Manager approved - process payment
        process_payment(expense)
        expense.status = "approved"
    else:
        # Manager rejected
        expense.status = "rejected"
        notify_employee(expense.employee_id, "Your expense was rejected.")
```

#### Real-World Example 4: Data Deletion Confirmation

**Scenario:** User asks AI to delete their account. This requires explicit confirmation.

```python
def handle_account_deletion_request(user_id: str, user_message: str):
    """Handle account deletion with human confirmation"""
    # Classify intent (Block 5: Control)
    intent = classify_intent(user_message)
    
    if intent.action == "delete_account":
        # CRITICAL: Don't delete immediately!
        # Require explicit confirmation
        
        # Step 1: Confirm with user
        confirmation_message = "Are you sure you want to delete your account? This action cannot be undone. Type 'DELETE MY ACCOUNT' to confirm."
        send_message(user_id, confirmation_message)
        
        # Step 2: Wait for explicit confirmation
        wait_for_confirmation(user_id, timeout=300)  # 5 minutes
        
    elif intent.action == "confirm_deletion":
        # User confirmed - but still require admin approval for safety
        request_admin_approval(user_id)
        
def request_admin_approval(user_id: str):
    """Require admin approval before deletion"""
    send_admin_notification(
        message=f"⚠️ Account Deletion Request:\nUser ID: {user_id}\n\n[Approve Deletion] [Reject]",
        callback_url=f"/api/admin/delete-account/{user_id}"
    )
    
    # Store in pending queue
    save_to_deletion_queue(user_id)

def handle_admin_approval(user_id: str, action: str):
    """Handle admin approval"""
    if action == "approve":
        # Admin approved - NOW delete account
        delete_user_account(user_id)
        log_action("account_deleted", user_id, admin_approved=True)
    else:
        # Admin rejected
        notify_user(user_id, "Your account deletion request was reviewed and your account will remain active.")
```

#### Key Takeaways:
- **Never automate high-stakes actions** without human oversight
- Use **approval workflows** for sensitive operations
- **Pause execution** and wait for human input
- Provide **clear options** (Approve/Reject/Edit)
- **Log all actions** for audit trails
- Consider **timeouts** - what if human doesn't respond?
- **Escalation paths** - what if approver is unavailable?

---

## Conclusion: Putting It Together

As you transition to an AI Engineer, remember that **AI agents are simply workflows** - directed acyclic graphs (DAGs) if you're being precise, or just graphs if you include loops. 

**Most steps in these workflows should be regular code - not LLM calls.**

You take a big problem, break it down into smaller problems, then solve each one using these building blocks chained together - that's how you build effective AI agents.

### How to Apply the Blocks

- **Need to understand the user?** → Block 1 & 5 (Intelligence & Control)
- **Need to remember context?** → Block 2 (Memory)
- **Need to get data?** → Block 3 (Tools)
- **Need to ensure it doesn't break?** → Block 4 & 6 (Validation & Recovery)
- **Need to be safe?** → Block 7 (Feedback)

### The Senior Workflow

When you face a new problem, don't ask "Which Agent framework should I use?" Instead, ask:

1. **Decompose:** Break the big problem into smaller problems
2. **Assign Blocks:** For each step, which block do I need?
3. **Orchestrate:** Connect the blocks using standard code (Python/TypeScript)

### Workflow Orchestration

These building blocks are the fundamental primitives. But how do you actually combine them? That's where **workflow orchestration** comes in:

- **Prompt chaining**: Connecting multiple LLM calls in sequence
- **Routing**: Using Control (Block 5) to direct flow based on conditions
- **Reflection**: Having the LLM review and improve its own output
- **Other agentic patterns**: That emerge when you combine these building blocks strategically

The key is that most of your workflow should be deterministic code. Only use LLM calls where "reasoning with context" is absolutely required.

### Example: Complete Customer Support System

Let's see how all blocks work together:

```python
class CustomerSupportSystem:
    """Complete system using all 7 blocks"""
    
    def __init__(self):
        self.conversations = {}  # Block 2: Memory
    
    def handle_customer_message(self, customer_id: str, message: str):
        # Block 2: Memory - Get conversation history
        if customer_id not in self.conversations:
            self.conversations[customer_id] = []
        
        history = self.conversations[customer_id]
        history.append({"role": "user", "content": message})
        
        # Block 5: Control - Classify intent
        intent = self.classify_intent(message)
        
        # Route based on intent
        if intent == "Question":
            response = self.answer_question(message, history)
        elif intent == "Complaint":
            response = self.handle_complaint(message, history)
        elif intent == "Request":
            response = self.handle_request(message, history)
        else:
            response = self.general_response(message, history)
        
        # Block 4: Validation - Ensure response is valid
        validated_response = self.validate_response(response)
        
        # Block 6: Recovery - Handle errors
        try:
            final_response = self.send_with_recovery(validated_response)
        except Exception as e:
            final_response = self.fallback_response()
        
        # Block 2: Memory - Save to history
        history.append({"role": "assistant", "content": final_response})
        
        return final_response
    
    def classify_intent(self, message: str):
        """Block 5: Control - Classify intent"""
        # Block 1: Intelligence Layer
        # Using traditional API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Classify: {message}"}],
            response_format={"type": "json_schema", "json_schema": {...}}  # Block 4: Validation
        )
        # Using new API (may need to handle response_format differently)
        # response_new = client.responses.create(
        #     model="gpt-4",
        #     input=f"Classify: {message}. Return JSON."
        # )
        return parse_intent(response)
    
    def answer_question(self, message: str, history: list):
        """Answer question using knowledge base"""
        # Block 3: Tools - Retrieve from knowledge base
        relevant_docs = retrieve_from_knowledge_base(message)
        
        # Block 1: Intelligence Layer - Generate answer
        # Using traditional API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=history + [{"role": "system", "content": f"Answer using: {relevant_docs}"}]
        )
        # Using new API - build conversation string from history
        # conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        # input_text = f"Answer using: {relevant_docs}\n\n{conversation_text}\nUser: {message}"
        # response_new = client.responses.create(model="gpt-4", input=input_text)
        return response.choices[0].message.content  # or response_new.output_text
    
    def handle_complaint(self, message: str, history: list):
        """Handle complaint - requires human approval"""
        # Block 1: Intelligence Layer - Draft response
        # Using traditional API
        draft = client.chat.completions.create(
            model="gpt-4",
            messages=history + [{"role": "system", "content": "Draft empathetic response"}]
        )
        # Using new API
        # conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        # input_text = f"Draft empathetic response\n\n{conversation_text}"
        # draft_new = client.responses.create(model="gpt-4", input=input_text)
        
        # Block 7: Feedback - Require approval
        return self.request_approval(draft.choices[0].message.content)  # or draft_new.output_text
    
    def send_with_recovery(self, response: str):
        """Block 6: Recovery - Send with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return send_message(response)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
```

### Final Thoughts

Don't get lost in the noise. Master these 7 blocks, and you can build anything:

1. ✅ **Intelligence Layer** - The AI engine
2. ✅ **Memory** - Context persistence
3. ✅ **Tools** - External integrations
4. ✅ **Validation** - Structured output
5. ✅ **Control** - Routing & decision making
6. ✅ **Recovery** - Error handling
7. ✅ **Feedback** - Human-in-the-loop

These blocks work together to create **reliable, production-ready AI systems** that work 99% of the time, not just in demos.

**Remember the core principle:** Take your big problem, break it down into smaller problems, then solve each one using these building blocks chained together. Most steps should be regular code - only use LLM calls where "reasoning with context" is absolutely required.

**The frameworks you see online aren't being used in production.** The most successful AI applications are built with these custom building blocks, not magic frameworks. Focus on mastering these fundamentals rather than chasing the latest framework.

---

## Additional Resources

### Practice Exercises

1. **Build a Simple Chatbot**
   - Implement Block 1 (Intelligence) and Block 2 (Memory)
   - Add conversation history management
   - Test with multi-turn conversations

2. **Create a Weather Assistant**
   - Implement Block 1 (Intelligence) and Block 3 (Tools)
   - Add a weather API tool
   - Handle tool calling and response formatting

3. **Build a Task Manager**
   - Implement Block 1, Block 4 (Validation), and Block 5 (Control)
   - Extract tasks from natural language
   - Classify tasks by priority and category

4. **Create a Customer Support Router**
   - Implement all 7 blocks
   - Route emails to appropriate teams
   - Add approval workflow for escalations

### Common Pitfalls to Avoid

1. **Over-relying on LLMs** - Use normal code when possible. Most steps should be deterministic code, not LLM calls
2. **Ignoring memory** - Forgetting to maintain conversation history
3. **Skipping validation** - Trusting unstructured LLM output
4. **No error handling** - Assuming APIs never fail
5. **Automating everything** - Forgetting human oversight for sensitive actions
6. **Poor context engineering** - Not preparing the right context for LLM calls
7. **Not breaking down problems** - Trying to solve everything with one big LLM call instead of decomposing into smaller steps
8. **Chasing frameworks** - Focusing on the latest framework instead of mastering the fundamental building blocks

### Next Steps

1. Start with Block 1 and Block 2 - build a simple chatbot
2. Add Block 3 - integrate one external tool
3. Add Block 4 - enforce structured output
4. Add Block 5 - implement routing logic
5. Add Block 6 - implement error handling
6. Add Block 7 - add approval workflows

Remember: **You don't need fancy frameworks. You need these 7 blocks.**

---

*This guide is designed for developers transitioning to AI Engineering. Master these fundamentals, and you'll be able to build production-ready AI systems that actually work.*
