from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

MAX_MESSAGES = 5

history = [{"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."}]

 
def add_new_message(history, message):
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": message})

    history = trim_history(history, MAX_MESSAGES)
    print(f"History length: {len(history)}")

    return history


def trim_history(history, max_messages):
    if len(history) > max_messages:
        print("History is too long, trimming...")
        # Always keep the system message at the beginning
        history = [history[0]] + history[-max_messages:]

    return history

for i in range(10):
    history = add_new_message(history, f"Hello, how are you? {i}")
    print(f"   Global list length: {len(history)}")

