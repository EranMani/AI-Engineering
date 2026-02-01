from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
    {"role": "user", "content": "Hi, my name is John."}
]

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
)

print(response.choices[0].message.content)

new_message = [
    {"role": "assistant", "content": response.choices[0].message.content},
    {"role": "user", "content": "What is my name?"}
]

messages.extend(new_message)

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
)

print(response.choices[0].message.content)