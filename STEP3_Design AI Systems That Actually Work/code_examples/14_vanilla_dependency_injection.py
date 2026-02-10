from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
client = OpenAI()

@dataclass
class User():
    name: str

def run_agent(user: User, question: str):
    sys_msg = f"User is {user.name}"
    result = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": question}
        ]
    )
    return result.choices[0].message.content

daniel = User(name="Daniel")
result = run_agent(daniel, "what is the weather in Tokyo?")
print(result)