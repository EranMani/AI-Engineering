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

    return draft_mail_review(mail), history

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
        if user_input.lower() in ["q", "quit", ""]:
            break

        current_input = user_input
        needs_new_draft = True 

        while True:
            # only pay openai if the flag needs new draft flag is raised
            if needs_new_draft:
                print("🤖 Generating draft...")
                draft, history = generate_draft(history, current_input)
                needs_new_draft = False

            # Always print the current draft 
            print(draft)

            feedback = input("Authorize this email? (yes/no/edit): ").lower()

            if feedback == "yes":
                print("🚀 EMAIL SENT SUCCESSFULLY.")
                break # break the inner loop, goes back to outer loop

            elif feedback == "no":
                print("🗑️ DRAFT DISCARDED.")
                break # break the inner loop, goes back to outer loop
                
            elif feedback == "edit":
                current_input = input("What is your feedback?")
                needs_new_draft = True
                # the loop restarts -> call generate draft again -> print new draft again

            else:
                print("Invalid command. Please type yes, no, or edit.")

if __name__ == "__main__":
    main(history)