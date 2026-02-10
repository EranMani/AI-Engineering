from openai import OpenAI
from dotenv import load_dotenv
import json
import random

load_dotenv()
client = OpenAI()

def roll_dice(bet: int) -> int:
    result = random.randint(1, 9)
    return result

tools = [{
    "type": "function",
    "function": {
        "name": "roll_dice",
        "description": "Returns 'Winner' if you bet 7",
        "parameters": {
            "type": "object",
            "properties": {
                "bet": {
                    "type": "integer"
                }
            },
            "required": ["bet"]
        }
    }
}]

result = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a dice game assistant."},
        {"role": "user", "content": "I bet 7. What is the result?"}
    ],
    tools=tools,
)

tool_calls = result.choices[0].message.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        if tool_name == "roll_dice":
            result = roll_dice(tool_args["bet"])
            print(f"The result of the dice is {result}")
        else:
            print(f"Unknown tool: {tool_name}")
else:
    print(result.choices[0].message.content)
