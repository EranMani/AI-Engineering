from openai import OpenAI
from dotenv import load_dotenv
import time
import random

load_dotenv()

client = OpenAI()

RETRY_LIMIT = 3

history = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."}
]

def call_llm_with_backoff(prompt, history):
    current_retry = 0

    while current_retry < RETRY_LIMIT:
        try:
            if random.random() < 0.9:
                raise Exception("Simulated API crash!")

            response = client.chat.completions.create(
                model="gpt-5-nano",
                messages=history,
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error: {e}")
            current_retry += 1
            time.sleep(2 ** current_retry)

    raise RuntimeError("Layer 1 Failed: Max retries reached")


def keyword_fallback(prompt):
    if "users" in prompt.lower():
        return "SELECT * FROM users"
    else:
        raise ValueError("Keyword not found")


def process_request(prompt, history):
    history.append(
        {"role": "user", "content": prompt}
    )

    try:
        print("🛡️ Attempting Layer 1 (LLM Intelligence)...")
        return call_llm_with_backoff(prompt, history)
    except Exception as e:
        print(f"⚠️ Layer 1 Failed: {e}")

        try:
            print("🛡️ Attempting Layer 2 (Keyword Fallback)...")
            return keyword_fallback(prompt)
        except Exception as e:
            print(f"⚠️ Layer 2 Failed: {e}")

            print("🛡️ Attempting Layer 3 (System Fallback)...")
            return "System Error: Query could not be processed. Please contact IT."

if __name__ == "__main__":
    print(process_request("Which users are currently in the database?", history))
    print(process_request("Get me the sales report", history))

