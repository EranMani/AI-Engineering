from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

sessions = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id


def get_chat_history(user_id):
    if not sessions.get(user_id):
        sessions[user_id] = [{"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."}]

    return sessions[user_id]

def chat(user_id, message):
    history = get_chat_history(user_id)
    history.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=history,
    )

    chat_answer = response.choices[0].message.content
    print(f"User {user_id}: {chat_answer}")
    history.append({"role": "assistant", "content": chat_answer})

user_a = User("user_123")
user_b = User("user_999")

chat(user_a.get_user_id(), "My name is Alice")
chat(user_b.get_user_id(), "My name is Bob")
chat(user_a.get_user_id(), "What is my name?")