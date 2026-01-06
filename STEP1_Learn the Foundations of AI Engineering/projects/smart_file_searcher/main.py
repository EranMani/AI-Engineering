import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# 1. Setup & Auth
load_dotenv()
client = OpenAI()

# --- PART A: DEFINE THE TOOL ---

# The Arguments Schema (What the model needs to provide)
class ListFilesArgs(BaseModel):
    directory: str = Field(description="The folder path to list files from (e.g., '.' for current folder)")

# The Actual Python Function (The "Worker")
def list_files(directory: str):
    """Lists files in a given directory."""
    try:
        # Safety: In a real app, you would restrict this to safe paths only!
        if not os.path.exists(directory):
            return "Error: Directory does not exist."
            
        files = os.listdir(directory)
        return json.dumps(files) # Return list as a string
    except Exception as e:
        return f"Error: {str(e)}"

# The Tool Definition (The "Menu" for the Model)
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Get a list of file names in a specific directory.",
            "parameters": ListFilesArgs.model_json_schema() # Auto-generated schema!
        }
    }
]

# --- PART B: THE CHAT LOOP ---

def chat_with_tools():
    # We start with a system message
    messages = [
        {"role": "system", "content": "You are a helpful file assistant. You can check files on the user's computer."}
    ]

    while True:
        # 1. Get User Input
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        # 2. First Call: Ask the Model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto" 
        )

        message = response.choices[0].message
        
        # 3. Check: Did the model want to use a tool?
        if message.tool_calls:
            print(f"🤖 (Model is thinking...) I need to run: {message.tool_calls[0].function.name}")
            
            # Append the model's "request" to history (It's required!)
            messages.append(message)

            for tool_call in message.tool_calls:
                # A. Parse the arguments using Pydantic
                args = ListFilesArgs.model_validate_json(tool_call.function.arguments)
                
                # B. Execute the actual function
                print(f"⚡ (System) Running list_files for: {args.directory}")
                result = list_files(args.directory)

                # C. Feed the result back to the model
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # 4. Second Call: Get the Final Answer
            final_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            print(f"AI: {final_response.choices[0].message.content}")
            
            # Save final answer to history so we can keep chatting
            messages.append(final_response.choices[0].message)

        else:
            # Model didn't use a tool, just replied
            print(f"AI: {message.content}")
            messages.append(message)

if __name__ == "__main__":
    print("--- AI File Searcher Started (Type 'quit' to exit) ---")
    chat_with_tools()