# OpenAI Python SDK: Complete Beginner's Guide

> **Your comprehensive guide to mastering the OpenAI API and Python SDK for AI Engineering**

This guide will take you from zero to building production-ready AI applications. We'll cover authentication, API interactions, structured outputs, memory management, function calling, streaming, and vision capabilities.

---

## Table of Contents

1. [Setup & Authentication](#1-setup--authentication-)
2. [Basic Chat Completions](#2-basic-chat-completions-)
3. [Structured Outputs](#3-structured-outputs-)
4. [Memory Management](#4-memory-management-)
5. [Function Calling (Tools & Agents)](#5-function-calling-tools--agents-)
6. [Streaming Responses](#6-streaming-responses-)
7. [Vision (Multimodal Inputs)](#7-vision-multimodal-inputs-)
8. [Best Practices & Common Pitfalls](#8-best-practices--common-pitfalls-)
9. [Project Ideas](#9-project-ideas-)

---

## 1. Setup & Authentication 🔐

### Why Environment Variables?

**The Problem:** Hardcoding API keys in your code is dangerous. If you share your code (e.g., on GitHub), anyone can steal your key and use your credits.

**The Solution:** Environment variables store sensitive data outside your code, keeping it secure.

### Installation

First, install the required libraries:

```bash
pip install openai python-dotenv
```

### Setting Up Your Environment

#### Step 1: Create a `.env` file

In your project root, create a file named `.env`:

```plaintext
OPENAI_API_KEY=sk-proj-1234567890abcdef...
```

**Important:** 
- No spaces around the `=` sign
- Never commit `.env` to version control (add it to `.gitignore`)
- The variable name must be exactly `OPENAI_API_KEY`

#### Step 2: Initialize the Client

The OpenAI SDK automatically looks for the `OPENAI_API_KEY` environment variable:

```python
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file into the system
load_dotenv()

# Initialize client (automatically finds OPENAI_API_KEY)
client = OpenAI()

print("Client initialized successfully!")
```

### How It Works

1. `load_dotenv()` reads your `.env` file and loads variables into your system's environment
2. `OpenAI()` automatically searches for `OPENAI_API_KEY` in the environment
3. No key appears in your code, keeping it secure

### Alternative: Direct Key Passing (Not Recommended)

While you can pass the key directly, it's not recommended for production:

```python
# ⚠️ Not recommended for production
client = OpenAI(api_key="sk-proj-...")
```

---

## 2. Basic Chat Completions 💬

### Understanding the Chat Model

The OpenAI API is essentially a "text predictor." You provide a conversation history, and the model predicts the next message in that conversation.

### Message Roles

Every message in a conversation has a **role** that tells the model who is speaking:

- **`system`**: Sets the AI's behavior, persona, and rules. This is like giving the AI a job description.
- **`user`**: The human's input/questions
- **`assistant`**: The AI's previous responses (for maintaining conversation history)

### Basic Request

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what Python is in one sentence."}
    ]
)

# Extract the response text
answer = response.choices[0].message.content
print(answer)
```

### Understanding the Response Structure

```python
response = client.chat.completions.create(...)

# Response object structure:
# response.choices[0]           # First (and usually only) choice
# response.choices[0].message    # The message object
# response.choices[0].message.content  # The actual text response
# response.choices[0].message.role     # Usually "assistant"
```

### Why Roles Matter

**System Role:** Provides instructions that persist throughout the conversation
- Sets personality, tone, constraints
- Defines the AI's "job"
- Critical for getting consistent, useful responses

**User Role:** The actual conversation content
- Questions, requests, information
- What the user wants to know or do

**Example:**

```python
# Without system role - generic response
response1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is Python?"}]
)

# With system role - specialized response
response2 = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a Python expert teaching beginners."},
        {"role": "user", "content": "What is Python?"}
    ]
)
# Response2 will be more beginner-friendly and educational
```

### Available Models

Common models you can use:

- `gpt-4o`: Latest, most capable model (recommended)
- `gpt-4o-mini`: Faster, cheaper, good for simple tasks
- `gpt-4-turbo`: Previous generation, still powerful
- `gpt-3.5-turbo`: Fastest, cheapest, good for simple tasks

---

## 3. Structured Outputs 🏗️

### The Problem with Text Responses

When you ask a model a question, it usually returns a paragraph of text:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me about the movie Inception."}]
)
# Returns: "Inception is a 2010 science fiction film directed by Christopher Nolan..."
```

**Problem:** This is just a string. You can't easily extract specific data (like the year, director, or genre) to use in your code.

### The Solution: Structured Outputs

Structured outputs force the model to return data in a specific format (like JSON) that matches a predefined schema. This makes the data reliable and easy to use in your code.

### Using Pydantic for Schema Definition

We use **Pydantic** (a Python library) to define the structure we want:

```python
from pydantic import BaseModel

# Define the "blueprint" for our data
class MovieInfo(BaseModel):
    title: str
    year: int
    genres: list[str]
    is_family_friendly: bool
```

### Requesting Structured Output

Use `.beta.chat.completions.parse()` instead of `.create()`:

```python
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client = OpenAI()

# Define the structure
class MovieInfo(BaseModel):
    title: str
    year: int
    genres: list[str]
    is_family_friendly: bool

# Request parsed output
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Structured outputs work best with newer models
    messages=[
        {"role": "system", "content": "You are a movie database helper."},
        {"role": "user", "content": "Tell me about Toy Story."}
    ],
    response_format=MovieInfo,  # The magic happens here
)

# Get the parsed object (already validated!)
movie = completion.choices[0].message.parsed

# Use it as a Python object
print(movie.title)              # "Toy Story"
print(movie.year)               # 1995 (integer, not string!)
print(movie.genres)             # ['Animation', 'Adventure', 'Comedy']
print(movie.is_family_friendly) # True
```

### Why Use `.parse()` Instead of `.create()`?

**Option A: Standard Method (Manual Parsing)**

```python
import json

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    response_format={"type": "json_object"}  # Just asks for generic JSON
)

# Get JSON string
json_string = response.choices[0].message.content
# Result: '{"title": "Toy Story", "year": "1995"}' 
# ⚠️ Note: year is a string, not an integer!

# Manual parsing
data = json.loads(json_string)

# ⚠️ If model made a typo or returned wrong format, this crashes!
print(data['year'])  # Might fail if key doesn't exist
```

**Option B: Parse Method (Automatic Validation)**

```python
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[...],
    response_format=MovieInfo  # Strict blueprint
)

# Already validated and typed!
movie = completion.choices[0].message.parsed
print(movie.year)  # Guaranteed to be an integer, guaranteed to exist
```

### Benefits of Structured Outputs

1. **Type Safety:** Data types are guaranteed (integers are integers, not strings)
2. **Validation:** Invalid data is caught immediately with clear errors
3. **IDE Support:** Your code editor can autocomplete fields
4. **Reliability:** No more parsing errors from malformed JSON

### Advanced Example: Nested Structures

```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Person(BaseModel):
    name: str
    age: int
    email: str
    address: Address
    phone: Optional[str] = None  # Optional field

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Extract information about John Doe, 30, living at 123 Main St, New York, 10001, email john@example.com"}
    ],
    response_format=Person
)

person = completion.choices[0].message.parsed
print(person.name)           # "John Doe"
print(person.address.city)   # "New York"
```

---

## 4. Memory Management 🧠

### The Stateless Problem

**Critical Concept:** The OpenAI API is **stateless**. It doesn't remember anything from one request to the next.

```python
# Request 1
response1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi, my name is Alex."}]
)

# Request 2
response2 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is my name?"}]
)

print(response2.choices[0].message.content)
# Output: "I don't know your name. You haven't told me yet."
```

The model has no memory of the first request!

### Solution: Conversation History

You must manually maintain a conversation history and send it with every request:

```python
# Initialize conversation history
history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# --- Turn 1 ---
history.append({"role": "user", "content": "Hi, my name is Alex."})

response1 = client.chat.completions.create(
    model="gpt-4o",
    messages=history
)

# Save the assistant's reply
assistant_msg = response1.choices[0].message
history.append(assistant_msg)
print(f"AI: {assistant_msg.content}")

# --- Turn 2 ---
history.append({"role": "user", "content": "What is my name?"})

response2 = client.chat.completions.create(
    model="gpt-4o",
    messages=history  # Send entire history
)

print(f"AI: {response2.choices[0].message.content}")
# Output: "Your name is Alex."
```

### The Chat Loop Pattern

Here's a complete interactive chat loop:

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Initialize history
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    # Get user input
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    # Send entire history to API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    # Get and display response
    assistant_message = response.choices[0].message
    print(f"AI: {assistant_message.content}")
    
    # ⚠️ CRITICAL: Add assistant's response to history
    messages.append(assistant_message)
```

### The Token Limit Problem

**Problem 1: Cost** 💸
- OpenAI charges per token (roughly per word)
- If you send 1,000 past messages + 1 new question, you pay for all 1,000 messages again
- Costs can spiral out of control

**Problem 2: Latency** 🐢
- The model must process all previous messages before generating a response
- Long histories = slow responses

**Problem 3: Context Window** 📏
- Every model has a maximum token limit (e.g., 128k tokens for GPT-4o)
- If history exceeds this, the API throws an error

### Memory Management Strategies

#### Strategy 1: Simple Truncation (First-In, First-Out)

```python
MAX_MESSAGES = 20

if len(messages) > MAX_MESSAGES:
    # Keep system message and last N messages
    messages = [messages[0]] + messages[-MAX_MESSAGES:]
```

**Problem:** You lose important early context (like the user's name).

#### Strategy 2: Summarization Memory (Recommended)

When history gets too long, summarize old messages into a single system message:

```python
def summarize_conversation(client, old_messages):
    """Summarize old messages into key facts"""
    summary_prompt = f"""
    Summarize the key facts from this conversation:
    {old_messages}
    
    Extract important information like:
    - User's name, preferences, or context
    - Important decisions made
    - Ongoing topics or tasks
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a conversation summarizer."},
            {"role": "user", "content": summary_prompt}
        ]
    )
    
    return response.choices[0].message.content

# Usage
MAX_MESSAGES = 50

if len(messages) > MAX_MESSAGES:
    # Get old messages (excluding system and recent)
    old_messages = messages[1:-10]  # Keep last 10, summarize the rest
    
    # Summarize
    summary = summarize_conversation(client, old_messages)
    
    # Replace old messages with summary
    messages = [
        messages[0],  # Keep system message
        {"role": "system", "content": f"Previous conversation context: {summary}"}
    ] + messages[-10:]  # Keep last 10 messages
```

#### Strategy 3: Token-Based Truncation

```python
import tiktoken  # Library to count tokens

def count_tokens(messages, model="gpt-4o"):
    """Count tokens in messages"""
    encoding = tiktoken.encoding_for_model(model)
    total = 0
    for msg in messages:
        total += len(encoding.encode(str(msg)))
    return total

MAX_TOKENS = 100000  # Leave room for response

while count_tokens(messages) > MAX_TOKENS:
    # Remove oldest non-system message
    if len(messages) > 2:
        messages.pop(1)  # Keep system message (index 0)
```

### Best Practices

1. **Always append assistant responses** to history before the next turn
2. **Monitor token count** for long conversations
3. **Use summarization** for persistent facts (names, preferences)
4. **Keep system message** at the beginning
5. **Implement a max history limit** to prevent runaway costs

---

## 5. Function Calling (Tools & Agents) 🛠️

### What is Function Calling?

Function calling (also called "Tools") allows the AI to request that your code execute specific functions. The AI doesn't run code itself—it asks you to run it, then uses the results.

### The Workflow

1. **Define:** You describe available functions to the model
2. **Decide:** Model returns a tool call request instead of text
3. **Execute:** Your Python code runs the function locally
4. **Report:** You send the result back to the model
5. **Answer:** Model generates the final response using the result

### Why It Runs Locally

**Important:** The code runs on **your computer**, not OpenAI's servers.

- **Security:** OpenAI never sees your database credentials or private code
- **Control:** You decide what functions are available
- **Cost:** Running code locally is free (API calls still cost money)

### Defining a Tool

#### Method 1: Manual JSON Schema (Verbose)

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Gets the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. Paris"
                }
            },
            "required": ["city"]
        }
    }
}]
```

#### Method 2: Using Pydantic (Recommended)

Much cleaner! We use the same Pydantic library from structured outputs:

```python
from pydantic import BaseModel, Field

# Define the arguments schema
class WeatherArgs(BaseModel):
    city: str = Field(description="The city name, e.g. Paris")

# Convert to OpenAI format
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a specific city.",
            "parameters": WeatherArgs.model_json_schema()  # Auto-generated!
        }
    }
]
```

### Implementing the Function

```python
def get_weather(city: str) -> str:
    """Gets the current weather for a city."""
    # In a real app, you'd call a weather API here
    # For demo purposes, we'll return mock data
    weather_data = {
        "Paris": "20°C, sunny",
        "Tokyo": "15°C, rainy",
        "New York": "10°C, cloudy"
    }
    return weather_data.get(city, f"Weather data not available for {city}")
```

### The Complete Function Calling Flow

```python
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json

load_dotenv()
client = OpenAI()

# --- Define Tool ---
class WeatherArgs(BaseModel):
    city: str = Field(description="The city name")

def get_weather(city: str) -> str:
    """Gets the current weather for a city."""
    weather_data = {
        "Paris": "20°C, sunny",
        "Tokyo": "15°C, rainy"
    }
    return weather_data.get(city, f"Weather not available for {city}")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "parameters": WeatherArgs.model_json_schema()
    }
}]

# --- The Chat Loop with Tools ---
messages = [
    {"role": "system", "content": "You are a helpful assistant with access to weather data."}
]

user_question = "What's the weather in Paris?"

messages.append({"role": "user", "content": user_question})

# Step 1: Send request with tools
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Let model decide whether to use tools
)

message = response.choices[0].message

# Step 2: Check if model wants to use a tool
if message.tool_calls:
    print(f"🤖 Model wants to run: {message.tool_calls[0].function.name}")
    
    # ⚠️ CRITICAL: Add model's request to history first
    messages.append(message)
    
    # Step 3: Execute each tool call
    for tool_call in message.tool_calls:
        # Parse arguments using Pydantic
        args = WeatherArgs.model_validate_json(tool_call.function.arguments)
        
        # Execute the function
        result = get_weather(args.city)
        print(f"⚡ Executed get_weather({args.city}) = {result}")
        
        # Step 4: Send result back to model
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,  # Links result to request
            "content": result
        })
    
    # Step 5: Get final answer
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools  # Keep tools available
    )
    
    print(f"AI: {final_response.choices[0].message.content}")
    messages.append(final_response.choices[0].message)
    
else:
    # Model answered without using tools
    print(f"AI: {message.content}")
    messages.append(message)
```

### Key Points

1. **`message.content` is None** when model uses a tool (it's waiting for results)
2. **Always append the tool call message** before appending tool results
3. **`tool_call_id`** links the result to the specific request
4. **Tool results are sent as strings** (JSON if needed)

### Multiple Tools Example

```python
from pydantic import BaseModel, Field

class CalculatorArgs(BaseModel):
    operation: str = Field(description="The operation: add, subtract, multiply, divide")
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

class WeatherArgs(BaseModel):
    city: str = Field(description="City name")

def calculate(operation: str, a: float, b: float) -> str:
    """Performs a calculation."""
    ops = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    result = ops.get(operation, lambda x, y: "Unknown operation")(a, b)
    return str(result)

def get_weather(city: str) -> str:
    """Gets weather for a city."""
    return f"25°C, sunny in {city}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Performs mathematical calculations.",
            "parameters": CalculatorArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets weather information.",
            "parameters": WeatherArgs.model_json_schema()
        }
    }
]

# The model will automatically choose the right tool based on the user's question
```

### Complete File Searcher Example

Here's a complete working example combining everything:

```python
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI()

# --- Tool Definition ---
class ListFilesArgs(BaseModel):
    directory: str = Field(description="The folder path to list files from")

def list_files(directory: str) -> str:
    """Lists files in a given directory."""
    try:
        if not os.path.exists(directory):
            return "Error: Directory does not exist."
        files = os.listdir(directory)
        return json.dumps(files)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [{
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Get a list of file names in a specific directory.",
        "parameters": ListFilesArgs.model_json_schema()
    }
}]

# --- Chat Loop ---
def chat_with_tools():
    messages = [
        {"role": "system", "content": "You are a helpful file assistant."}
    ]
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        messages.append({"role": "user", "content": user_input})
        
        # First call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            print(f"🤖 Running: {message.tool_calls[0].function.name}")
            messages.append(message)
            
            for tool_call in message.tool_calls:
                args = ListFilesArgs.model_validate_json(tool_call.function.arguments)
                result = list_files(args.directory)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final answer
            final_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            print(f"AI: {final_response.choices[0].message.content}")
            messages.append(final_response.choices[0].message)
        else:
            print(f"AI: {message.content}")
            messages.append(message)

if __name__ == "__main__":
    chat_with_tools()
```

---

## 6. Streaming Responses 🌊

### Why Streaming?

**Problem:** By default, your code waits for the entire response before showing anything. For long responses, this feels slow and unresponsive.

**Solution:** Streaming shows text as it's generated, character by character (like ChatGPT).

### The Concept

- **Batch Mode (Default):** Order a pizza, wait 20 minutes, entire pizza arrives
- **Stream Mode:** Sushi belt - plates arrive one by one, you start eating immediately

### Basic Streaming

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

print("Question: Tell me a short story about a brave toaster.")
print("Answer: ", end="", flush=True)

# Enable streaming
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a short story about a brave toaster."}],
    stream=True  # The magic switch
)

# Iterate over chunks as they arrive
for chunk in stream:
    # Extract the text piece (delta = change since last chunk)
    if chunk.choices[0].delta.content is not None:
        text_piece = chunk.choices[0].delta.content
        print(text_piece, end="", flush=True)

print("\n\n--- Stream Finished ---")
```

### Understanding Delta vs. Message

- **`message.content`**: Complete final message (used in non-streaming)
- **`delta.content`**: The tiny piece of text in this chunk (1-3 tokens)

### Why the `is not None` Check?

Some chunks contain only metadata (role, finish_reason) and have `content=None`. Printing `None` would break your output.

### Streaming with Memory

Since streaming doesn't give you a complete message object, you must manually collect the text:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

user_input = input("You: ")
messages.append({"role": "user", "content": user_input})

print("AI: ", end="", flush=True)
full_response = ""

stream = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        text_piece = chunk.choices[0].delta.content
        print(text_piece, end="", flush=True)
        full_response += text_piece  # Collect pieces

print()  # New line after stream

# Save to history for next turn
messages.append({"role": "assistant", "content": full_response})
```

### Streaming with Tools

Streaming works with function calling, but it's more complex:

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    stream=True
)

full_content = ""
tool_calls = []

for chunk in stream:
    delta = chunk.choices[0].delta
    
    if delta.content:
        print(delta.content, end="", flush=True)
        full_content += delta.content
    
    if delta.tool_calls:
        # Tool calls come in chunks too
        for tool_call_delta in delta.tool_calls:
            idx = tool_call_delta.index
            if len(tool_calls) <= idx:
                tool_calls.append({"id": "", "function": {"name": "", "arguments": ""}})
            
            if tool_call_delta.id:
                tool_calls[idx]["id"] = tool_call_delta.id
            if tool_call_delta.function.name:
                tool_calls[idx]["function"]["name"] = tool_call_delta.function.name
            if tool_call_delta.function.arguments:
                tool_calls[idx]["function"]["arguments"] += tool_call_delta.function.arguments

# After stream completes, check for tool calls
if tool_calls:
    # Execute tools and get final response (similar to non-streaming)
    ...
```

### Best Practices

1. **Always use `flush=True`** when printing to show text immediately
2. **Collect text** if you need to save to history
3. **Handle None values** to avoid crashes
4. **Use streaming for UX**, batch mode for reliability

---

## 7. Vision (Multimodal Inputs) 👁️

### What is Vision?

GPT-4o can "see" images. You can send photos, screenshots, or diagrams and ask the model to analyze them.

### The Content Format Change

Instead of a simple string, `content` becomes a **list of dictionaries**:

```python
# Text only (old way)
"content": "Hello, how are you?"

# Text + Image (new way)
"content": [
    {"type": "text", "text": "What is in this image?"},
    {"type": "image_url", "image_url": {"url": "..."}}
]
```

### Method 1: Image URLs

If the image is already online, just use the URL:

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is weird about this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/3/30/Echo_Park_Lake_with_Downtown_Los_Angeles_Skyline.jpg"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```

### Method 2: Local Files (Base64 Encoding)

For local files, you must convert the image to Base64 (a text representation of binary data):

```python
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def encode_image(image_path):
    """Reads a file and converts it to a Base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Encode your image
image_path = "test.jpg"
base64_image = encode_image(image_path)

# Send request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in detail."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```

### Understanding Base64

Base64 converts binary data (images) into text that can be sent over HTTP. The format is:

```
data:image/jpeg;base64,<base64_string>
```

Or for PNG:
```
data:image/png;base64,<base64_string>
```

### Multiple Images

You can send multiple images in one request:

```python
content = [
    {"type": "text", "text": "Compare these two images."},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image1}"}},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image2}"}}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": content}]
)
```

### Vision + Structured Outputs

Combine vision with structured outputs for powerful data extraction:

```python
from pydantic import BaseModel

class ReceiptInfo(BaseModel):
    total_amount: float
    date: str
    merchant_name: str
    items: list[str]

# Encode receipt image
base64_image = encode_image("receipt.jpg")

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all information from this receipt."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        }
    ],
    response_format=ReceiptInfo
)

receipt = completion.choices[0].message.parsed
print(f"Total: ${receipt.total_amount}")
print(f"Merchant: {receipt.merchant_name}")
```

### Supported Image Formats

- JPEG/JPG
- PNG
- WebP
- GIF (first frame only)

### Image Size Limits

- Maximum file size: 20MB
- Maximum resolution: Varies by model (GPT-4o supports high resolution)

### Use Cases

1. **Document Analysis:** Extract text from images, analyze forms
2. **Medical Imaging:** Analyze X-rays, scans (with proper validation)
3. **Quality Control:** Inspect products, detect defects
4. **Accessibility:** Describe images for visually impaired users
5. **Content Moderation:** Detect inappropriate content

---

## 8. Best Practices & Common Pitfalls ⚠️

### Security Best Practices

1. **Never commit API keys** to version control
   ```bash
   # Add to .gitignore
   .env
   *.env
   ```

2. **Use environment variables** for all secrets
3. **Rotate keys** if accidentally exposed
4. **Set usage limits** in OpenAI dashboard

### Error Handling

Always handle API errors gracefully:

```python
from openai import OpenAI, APIError, RateLimitError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    print("Rate limit exceeded. Please wait.")
except APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Cost Management

1. **Monitor token usage:**
   ```python
   response = client.chat.completions.create(...)
   print(f"Tokens used: {response.usage.total_tokens}")
   print(f"Prompt tokens: {response.usage.prompt_tokens}")
   print(f"Completion tokens: {response.usage.completion_tokens}")
   ```

2. **Set max_tokens** to limit response length:
   ```python
   response = client.chat.completions.create(
       model="gpt-4o",
       messages=[...],
       max_tokens=100  # Limit response to 100 tokens
   )
   ```

3. **Use cheaper models** for simple tasks (`gpt-4o-mini` vs `gpt-4o`)

### Common Mistakes

#### Mistake 1: Forgetting to Append Assistant Messages

```python
# ❌ WRONG
messages.append({"role": "user", "content": "Hello"})
response = client.chat.completions.create(...)
# Missing: messages.append(response.choices[0].message)
# Next request won't have context!

# ✅ CORRECT
messages.append({"role": "user", "content": "Hello"})
response = client.chat.completions.create(...)
messages.append(response.choices[0].message)  # Critical!
```

#### Mistake 2: Not Adding Tool Call Message Before Tool Result

```python
# ❌ WRONG
if message.tool_calls:
    result = run_tool(...)
    messages.append({"role": "tool", ...})  # Missing the tool call message!

# ✅ CORRECT
if message.tool_calls:
    messages.append(message)  # Add tool call first
    result = run_tool(...)
    messages.append({"role": "tool", ...})
```

#### Mistake 3: Not Handling None in Streaming

```python
# ❌ WRONG
for chunk in stream:
    print(chunk.choices[0].delta.content)  # Crashes if None

# ✅ CORRECT
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content)
```

#### Mistake 4: Hardcoding Model Names

```python
# ❌ WRONG
model = "gpt-4o"  # Hard to change

# ✅ CORRECT
model = os.getenv("OPENAI_MODEL", "gpt-4o")  # Configurable
```

### Performance Tips

1. **Use streaming** for better UX
2. **Batch requests** when possible
3. **Cache responses** for repeated queries
4. **Use appropriate models** (don't use GPT-4o for simple tasks)

### Testing

Always test your code with different inputs:

```python
def test_chat():
    messages = [{"role": "user", "content": "Hello"}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    assert response.choices[0].message.content is not None
    print("✅ Test passed")
```

---

## 9. Project Ideas 💡

### Beginner Projects

1. **Simple Chatbot**
   - Basic chat loop with memory
   - System prompts for different personas

2. **Text Summarizer**
   - Input: Long text
   - Output: Structured summary (using structured outputs)

3. **Code Explainer**
   - Input: Code snippet
   - Output: Explanation in plain English

### Intermediate Projects

4. **Smart File Searcher** (We built this!)
   - Tool: `list_files(directory)`
   - Tool: `read_file(filename)`
   - Ask: "What Python files mention 'OpenAI'?"

5. **Expense Tracker**
   - Vision: Upload receipt photos
   - Structured Output: Extract amount, date, merchant
   - Save to CSV/database

6. **Document Q&A**
   - Upload documents (PDF, text)
   - Ask questions about content
   - Use embeddings for search (advanced)

### Advanced Projects

7. **AI Agent with Multiple Tools**
   - Weather API
   - Calendar integration
   - Email sending
   - Database queries

8. **Code Review Assistant**
   - Input: Code diff
   - Output: Structured feedback (bugs, improvements, style)

9. **Content Moderation System**
   - Check user input for harmful content
   - Use moderation API
   - Block or flag inappropriate content

### Combining Concepts

**The Ultimate Project: AI Personal Assistant**

- **Authentication:** Secure API key management
- **Chat:** Natural conversation
- **Structured Outputs:** Extract tasks, dates, reminders
- **Memory:** Remember preferences, past conversations
- **Function Calling:** 
  - Send emails
  - Check calendar
  - Search files
  - Get weather
- **Streaming:** Real-time responses
- **Vision:** Analyze screenshots, photos

---

## Summary: Your Learning Journey 🎓

You've progressed from a total beginner to an AI Application Developer. Here's what you've mastered:

### ✅ Core Concepts

1. **Authentication & Security**
   - Environment variables
   - `.env` files
   - Secure key management

2. **Basic Chat Completions**
   - Message roles (system, user, assistant)
   - Model selection
   - Response handling

3. **Structured Outputs**
   - Pydantic schemas
   - `.parse()` method
   - Type-safe data extraction

4. **Memory Management**
   - Conversation history
   - Token limits
   - Summarization strategies

5. **Function Calling**
   - Tool definitions
   - Local execution
   - Multi-step workflows

6. **Streaming**
   - Real-time responses
   - Delta handling
   - UX improvements

7. **Vision**
   - Image encoding
   - Multimodal inputs
   - Base64 conversion

### 🚀 Next Steps

1. **Build a project** combining multiple concepts
2. **Explore the Assistants API** (managed memory and threads)
3. **Learn Embeddings** for document search (RAG)
4. **Study Audio APIs** (Whisper for transcription, TTS for speech)
5. **Explore Image Generation** (DALL-E 3)

### 📚 Additional Resources

- [OpenAI Python SDK Documentation](https://github.com/openai/openai-python)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## Quick Reference Cheat Sheet

### Basic Chat
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### Structured Output
```python
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[...],
    response_format=MyPydanticModel
)
data = completion.choices[0].message.parsed
```

### Streaming
```python
stream = client.chat.completions.create(..., stream=True)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Vision
```python
messages=[{
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe this"},
        {"type": "image_url", "image_url": {"url": "..."}}
    ]
}]
```

### Function Calling
```python
response = client.chat.completions.create(..., tools=tools)
if response.choices[0].message.tool_calls:
    # Execute tool and send result back
```

---

**Congratulations!** You now have the fundamental skills to build production-ready AI applications. Keep practicing, building projects, and exploring new features. The field of AI engineering is rapidly evolving—stay curious and keep learning! 🚀

