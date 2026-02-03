from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

history = [
    {"role": "system", "content": "You are a helpful assistant that generates email drafts for a sales team to review and approve."},
]

class EmailDraft(BaseModel):
    recipient: str = Field(description="The recipient of the email")
    subject: str = Field(description="The subject of the email")
    body: str = Field(description="The body of the email")

def generate_draft(history: list, user_input: str):
    history.append(
        {"role": "user", "content": user_input}
    )

    response = client.beta.chat.completions.parse(
        model="gpt-5-nano",
        messages=history,
        response_format=EmailDraft
    )

    mail = response.choices[0].message.parsed

    return draft_mail_review(mail)

def draft_mail_review(mail: EmailDraft):
    draft = f"""
        --- DRAFT --- 
        To: {mail.recipient}
        Subject: {mail.subject}
        Body: {mail.body}
    """

    return draft

def main(history: list):
    while True:
        user_input = input("What is your email request?")
        if user_input == "q" or user_input == "quit" or not user_input:
            break

        draft = generate_draft(history, user_input)
        print(draft)
        
        feedback = input("Authorize this email? (y/n): ")
        if feedback == "y":
            print("🚀 EMAIL SENT SUCCESSFULLY.")
        elif feedback == "n":
            print("🗑️ DRAFT DISCARDED.")

if __name__ == "__main__":
    main(history)