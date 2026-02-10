from pydantic_ai import Agent
from pydantic import BaseModel, Field
import asyncio
from dotenv import load_dotenv

load_dotenv()

reviewers_config = [
    {"role": "Security", "focus": "vulnerabilities and safety"},
    {"role": "Performance", "focus": "speed and memory usage"},
    {"role": "Maintainability", "focus": "readability and clean code"}
]

class ReviewResult(BaseModel):
    role: str = Field(description="The role of the reviewer")
    focus: str = Field(description="The focus of the reviewer")
    details: str = Field(description="The details of the review")

def create_reviewer_agent(role: str, focus: str):
    agent = Agent(
        model="gpt-5-nano",
        system_prompt=f"You are a {role} code reviewer. Your focus is on {focus}.",
        output_type=ReviewResult
    )

    return agent

async def main():
    bad_code = """
    def calculate_total(items):
        total = 0
        for item in item:
            total += item['price']
        return total
    """

    reviewers = [create_reviewer_agent(reviewer["role"], reviewer["focus"]) for reviewer in reviewers_config]
    tasks = [reviewer.run(bad_code) for reviewer in reviewers]
    
    results = await asyncio.gather(*tasks)
    for result in results:
        data = result.output
        print(f"Reviewer: {data.role}, Focus: {data.focus}")
        print(f"Details: {data.details}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())