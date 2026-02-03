from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

client = OpenAI()

MAX_RETRIES = 3

class ChatResponse(BaseModel):
    mood: Literal["Happy", "Sad", "Neutral", "Angry"] = Field(description="The mood of the response")
    content: str = Field(description="The content of the response")

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant that can respond to user messages with a mood and content."},
]

def add_new_message(history: list, role: str, content: str):
    history.append({"role": role, "content": content})
    return history

def get_response(history: list):
    temp_history = history.copy()
    current_retry = 0

    while current_retry < MAX_RETRIES:
        try:
            response = client.beta.chat.completions.parse(
                model="gpt-5-nano",
                messages=temp_history,
                response_format=ChatResponse
            )

            return response.choices[0].message.parsed

        except Exception as e:
            print(f"Error: {e}")
            current_retry += 1
            temp_history.append({"role": "user", "content": f"Response failed {e}. You must try again!"})

def main(conversation_history):
    while True:
        user_input = input("write something: ")
        if user_input:
            conversation_history = add_new_message(conversation_history, "user", user_input)
            result = get_response(conversation_history)
            print(result)
            if result:
                conversation_history = add_new_message(conversation_history, "assistant", result.content)

            print(conversation_history)

if __name__ == "__main__":
    main(conversation_history)