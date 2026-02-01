from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messy_data = "policy_v2_final_FINAL.txt: returns are allowed within 30 days but only if u have the receipt.. wait, unless its a holiday then 60 days. also electronics require original box. manager approval needed for >$500. shipping is user paid unless defective."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can answer clients questions about electric products return policies."},
        {"role": "user", "content": f"Context: {messy_data}.\n\nQuestion: Can I return a laptop after 45 days if I bought it during christmas?"}
    ]
)

print(response.choices[0].message.content)