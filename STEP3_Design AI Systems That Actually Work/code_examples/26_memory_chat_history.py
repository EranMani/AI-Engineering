from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

chat_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
    output_type=str
)

history = []

def main(history):
    while True:
        user_input = input("Ask away: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        response = chat_agent.run_sync(user_prompt=user_input, message_history=history)
        print(response.output)
        history += response.new_messages()

if __name__ == "__main__":
    main(history)

        