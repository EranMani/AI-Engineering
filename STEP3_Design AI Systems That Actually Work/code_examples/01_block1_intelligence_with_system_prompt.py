from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are Shakespeare who answer questions only using a riddle or poem."},
        {"role": "user", "content": "what is the sum of 50 + 50?"}
    ]
)

print(response.choices[0].message.content)