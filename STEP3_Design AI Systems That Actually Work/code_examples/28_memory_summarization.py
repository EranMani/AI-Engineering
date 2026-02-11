from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart
from pydantic import TypeAdapter
from dotenv import load_dotenv
import os

RUN_ONCE = False

MAX_HISTORY_LENGTH = 10 # Trigger compression when history hits this size
KEEP_RECENT = 4 # Number of recent messages to keep exactly as they are

load_dotenv()

# convert list of messages to/from JSON
message_adapter = TypeAdapter(list[ModelMessage])

chat_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
    output_type=str
)

summarize_message_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a helpful assistant that can summarize messages from a json file.",
    output_type=str
)

history = []


def compress_history(history: list[ModelMessage]) -> list[ModelMessage]:
    if len(history) <= MAX_HISTORY_LENGTH:
        return history
    
    print("\n[System: Compressing memory to save context...]")

    old_messages = history[:-KEEP_RECENT]
    recent_messages = history[-KEEP_RECENT:]
    old_messages_text = message_adapter.dump_json(old_messages).decode("utf-8")
    summary_response = summarize_message_agent.run_sync(user_prompt=f"Summarize the following messages into a concise summary: {old_messages_text}")
    summary_text = summary_response.output

    summary_message = ModelRequest(
        parts=[UserPromptPart(content=f"System Note - Summary of previous conversation: {summary_text}")]
    )

    compressed_history = [summary_message] + recent_messages 
    return compressed_history

def save_history(history):
    history = message_adapter.dump_json(history)
    history_file = os.path.join(os.path.dirname(__file__), "history.json")
    with open(history_file, "wb") as f:
        f.write(history)

def load_history():
    history_file = os.path.join(os.path.dirname(__file__), "history.json")
    if not os.path.exists(history_file):
        return []

    with open(history_file, "rb") as f:
        history = message_adapter.validate_json(f.read())
        return history

def main(run_once: bool = False):
    history = load_history()
    while True:
        if not run_once and history:
            run_once = True
            history_text = message_adapter.dump_json(history).decode("utf-8")
            response = summarize_message_agent.run_sync(user_prompt=f"Summarize the following messages into a warm and very personal wlecome back message for the user: {history_text}")
            print(response.output)

        user_input = input("Ask away: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        response = chat_agent.run_sync(user_prompt=user_input, message_history=history)
        print(response.output)
        history += response.new_messages()
        history = compress_history(history)
        save_history(history)

if __name__ == "__main__":
    main(RUN_ONCE)

        