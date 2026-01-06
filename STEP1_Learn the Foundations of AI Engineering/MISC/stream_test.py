import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("Question: Tell me a short story about a brave toaster.")
print("Answer: ", end="", flush=True) # Prepare the terminal line

full_response = ""

# 1. The Request (Note the stream=True argument)
stream = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "Tell me a funny joke about AI"}],
    stream=True, # <--- The Magic Switch
)

# 2. The Loop (Iterate over the chunks as they arrive)
for chunk in stream:
    # 3. Extract the tiny piece of text (The "Delta")
    if chunk.choices[0].delta.content is not None:
        text_piece = chunk.choices[0].delta.content
        
        # 4. Print without a newline
        print(text_piece, end="", flush=True)

        full_response += text_piece

print(f"full_response: {full_response}")
print("\n\n--- Stream Finished ---")