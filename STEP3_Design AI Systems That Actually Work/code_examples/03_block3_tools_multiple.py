"""
03_block3_tools_multiple.py
===========================

Purpose:
    Demonstrates how to give an LLM multiple tools (functions) and handle the 
    "Execution Loop" where the AI selects a tool, we run it, and feed the result back.

Key Concepts:
    1. Tool Schema: The JSON definition that tells the LLM what functions are available.
    2. Dynamic Dispatch: Using a dictionary (`available_functions`) to map string names 
       (from the AI) to actual Python functions.
    3. The Execution Loop (The "Ping Pong"):
       - Step 1: User asks a question.
       - Step 2: AI sees it can't answer, so it requests a tool call (returns `tool_calls`).
       - Step 3: We (the code) catch this request.
       - Step 4: We MUST append the AI's request to the history (so it remembers it asked).
       - Step 5: We run the Python function locally.
       - Step 6: We append the result as a new message with role="tool".
       - Step 7: We call the API again so the AI can read the result and answer the user.

Critical Implementation Details:
    - The `tool_call_id` is mandatory. The AI uses it to match the answer to the question.
    - You must include the original `assistant` message in history, or the API will 
      reject the `tool` message as an "orphan" answer.
    - Always handle the loop (iterate over `tool_calls`) because the AI might want 
      to run multiple tools at once (e.g., "Check weather in Paris AND London").
"""

from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
    {"role": "user", "content": "What is the weather and time in New York?"}
]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name to get the weather for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the time of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name to get the time for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and 25 degrees Celsius."

def get_time(city: str) -> str:
    return f"The time in {city} is 2:00 PM."

available_functions = {
    "get_weather": get_weather,
    "get_time": get_time
}

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
)

tool_calls = response.choices[0].message.tool_calls
print(tool_calls)

if tool_calls:
    messages.append(response.choices[0].message)

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        print(f"Executing local function: {tool_name} with {tool_args}")
        tool_result = available_functions[tool_name](**tool_args)
        print(f"Tool result: {tool_result}")

        messages.append({
            "role": "tool", "content": tool_result, "tool_call_id": tool_call.id
        })

    final_response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        tools=tools
    )

    print("Final Answer:", final_response.choices[0].message.content)