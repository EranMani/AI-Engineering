from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
    {"role": "user", "content": "What is the weather in Paris?"}
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
    }
]

def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and 25 degrees Celsius."

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
    tools=tools,
)

# NOTE: When AI calls a tool, .content is usually None

tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    # 'response.choices[0].message' is a special Python Object (specifically ChatCompletionMessage)
    # When you append this Object to the messages list, the OpenAI SDK automatically converts it into the correct JSON format for you behind the scenes
    """
    ChatCompletionMessage(
        role='assistant', 
        content=None, 
        tool_calls=[...]
    )
    """
    messages.append(response.choices[0].message)

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        
        print(f"Executing local function: {tool_name} with {tool_args}")
        
        # Execute the function
        tool_result = get_weather(tool_args["city"])

        # 2. Append the result to history
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        })

    final_response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        tools=tools
    )

    print("Final Answer:", final_response.choices[0].message.content)


