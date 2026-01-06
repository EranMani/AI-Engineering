import os
from openai import OpenAI
from dotenv import load_dotenv
from schemas import SentimentResult
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

# init client
client = OpenAI()

@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(Exception)
)
def analyze_text(text: str) -> SentimentResult:
    response = client.responses.parse(
        model="gpt-4o-mini",  # or "gpt-4o" - "gpt-5-mini" doesn't exist
        input=f"Analyze this text: {text}",  # input is a string, not a list
        text_format=SentimentResult,  # Pass the Pydantic class directly, not model_json_schema()
        timeout=5.0
    )

    return response.output_text # Access via .parsed, not .output

result = analyze_text("Im happy")
print(f"The result is: {result}")