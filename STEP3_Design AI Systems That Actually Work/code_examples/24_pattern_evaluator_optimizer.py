from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3

# --- Models ---
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")

class Evaluation(BaseModel):
    score: int = Field(description="The score of the joke", ge=1, le=10)
    feedback: str = Field(description="The feedback on the joke")

# --- Agents ---
generator_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a comedian. Write a joke about the given topic.",
    output_type=Joke
)

evaluator_agent = Agent(
    model="openai:gpt-5-nano",
    system_prompt="You are a harsh critic. Rate the joke. Be honest.",
    output_type=Evaluation
)

def main():
    print("--- 🎭 The AI Comedy Club is Open! ---")
    
    current_retry = 0
    # We store the *entire object* so we have setup + punchline
    best_joke = None 
    feedback = ""

    while current_retry <= MAX_RETRIES:
        
        # --- STEP 1: Construct the Prompt ---
        if best_joke is None:
            # First try: Fresh generation
            prompt = "Write a joke about Python programming. It must be funny."
        else:
            # Retry: Refinement based on FEEDBACK
            print(f"   ... Refining based on feedback: '{feedback}'")
            prompt = (
                f"Your previous joke was: '{best_joke.setup} - {best_joke.punchline}'.\n"
                f"The critic said: '{feedback}'.\n"
                "Write a BETTER version of this joke (or a new one) that addresses this critique."
            )

        # --- STEP 2: Generate ---
        result_joke = generator_agent.run_sync(prompt)
        joke_data = result_joke.output # .data (or .output depending on version)
        
        print(f"\n[Attempt {current_retry+1}] Joke: {joke_data.setup} ... {joke_data.punchline}")

        # --- STEP 3: Evaluate ---
        # Evaluate the WHOLE joke
        eval_prompt = f"Setup: {joke_data.setup}\nPunchline: {joke_data.punchline}"
        result_eval = evaluator_agent.run_sync(eval_prompt)
        eval_data = result_eval.output
        
        print(f"   [Critic] Score: {eval_data.score}/10. Feedback: {eval_data.feedback}")

        # --- STEP 4: The Gate ---
        if eval_data.score >= 8:
            print("\n✅ SUCCESS! We have a winner!")
            print(f"Final Joke: {joke_data.setup} \n{joke_data.punchline}")
            break
        
        # --- STEP 5: Prepare for Next Loop ---
        current_retry += 1
        best_joke = joke_data
        feedback = eval_data.feedback

        if current_retry >= MAX_RETRIES:
            print("\n❌ Max retries reached. The comedian is out of material.")
            break

if __name__ == "__main__":
    main()