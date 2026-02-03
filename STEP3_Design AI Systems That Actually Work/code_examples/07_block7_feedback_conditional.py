from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

client = OpenAI()

class Action(str, Enum):
    SEND_EMAIL = "send_email"
    REPLY_TEXT = "reply_text"

RISK_THRESHOLD = 7


history = [
    {"role": "system", "content": "You are a helpful assistant that helps users with their email and text messages."},
]

class Command(BaseModel):
    action: Action = Field(description="The action to take")
    content: str = Field(description="The content of the message")
    
    risk_score: int = Field(
        description="""
        A score from 1-10 indicating the consequence of this action.
        - 10 (CRITICAL): Involves money, sensitive privacy data, or HIGH REPUTATIONAL DAMAGE (e.g., angry clients, legal threats).
        - 7-9 (HIGH): External communication with executives or major partners.
        - 1-6 (LOW): Internal chitchat, greetings, or low-stakes scheduling.
        """, 
        ge=1, le=10
    )


def get_command(history: list, user_input: str):
    history.append({"role": "user", "content": user_input})

    response = client.beta.chat.completions.parse(
        model="gpt-5-nano",
        messages=history,
        response_format=Command
    )
    return response.choices[0].message.parsed, history

def main(history: list):
    while True:
        user_input = input("\nEnter command (or 'q' to quit): ")
        if user_input.lower() in ["q", "quit", ""]:
            break

        print("🧠 Analyzing Risk...")
        cmd, history = get_command(history, user_input)

        print(f"🤖 Command: {cmd.action.value} - Risk: {cmd.risk_score}/10")

        if cmd.risk_score >= RISK_THRESHOLD:
            print(f"⚠️ HIGH RISK ACTION DETECTED. Human approval required.")
            confirm = input(f"Authorize '{cmd.content}'? (y/n): ").lower()

            if confirm == "y":
                print("✅ APPROVED. Executing securely.")
            else:
                print("🛑 BLOCKED. Action cancelled.")
        else:
            print(f"⚡ LOW RISK. Auto-approving...")
            print(f"🚀 Executed: {cmd.content}")

if __name__ == "__main__":
    main(history)