from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

MAX_RETRIES = 3

conversation_history = [
    {"role": "system", "content": "You are a resilient AI assistant."}
]

def add_new_message(history: dict, role: str, content: str):
    history.append({"role": role, "content": content})
    return history

def get_response_with_retry(history: list):
    current_retry = 0
    while current_retry < MAX_RETRIES:
        try:
            response = client.chat.completions.create(
                model="gpt-5-nano",
                messages=history
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            current_retry += 1
            print(f"Retrying... ({current_retry}/{MAX_RETRIES})")

            if current_retry >= MAX_RETRIES:
                print("Max retries reached. Returning None.")
                return None

def main(conversation_history):
    while True:
        user_input = input("Write something:")
        conversation_history = add_new_message(conversation_history, "user", user_input)
        result = get_response_with_retry(conversation_history)
        if result:
            print(f"Assistant: {result}")
            conversation_history = add_new_message(conversation_history, "assistant", result)
        else:
            print("Failed to get response. Please try again.")

if __name__ == "__main__":
    main(conversation_history)
