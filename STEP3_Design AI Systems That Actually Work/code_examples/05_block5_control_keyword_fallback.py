"""
05_block5_control_keyword_fallback.py
=====================================

Purpose:
    Demonstrates a "Hybrid Router" that combines the intelligence of an LLM 
    with the deterministic safety of keyword matching.

Key Patterns:
    1. The Confidence Check:
       - LLMs provide a `confidence` (or probability) score.
       - If `confidence < THRESHOLD`, we declare the LLM "unsafe" or "unsure."

    2. The Fallback Layer (Safety Net):
       - When the LLM fails the confidence check, we execute a deterministic 
         Python function (`run_keyword_fallback`).
       - This ensures that ambiguous queries (which might cause the LLM to hallucinate) 
         are caught by hard-coded rules.

Trade-off Analysis:
    - **LLM First (Fallback):** Higher accuracy (understands context/negation), higher cost.
    - **Keyword First (Gateway):** Lower cost, lower accuracy (can be tricked by "not a refund").
    - This script uses the Fallback pattern to prioritize accuracy.
"""

from enum import Enum
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

CONFIDENCE_THRESHOLD = 0.6

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT_ACCESS = "account_access"
    UNKNOWN = "unknown"

class Classification(BaseModel):
    category: TicketCategory = Field(description="The category of the ticket")
    confidence: float = Field(description="The confidence score for the category")

def run_keyword_fallback(text: str) -> Classification:
    if "reset" in text.lower() or "password" in text.lower():
        return Classification(category=TicketCategory.ACCOUNT_ACCESS, confidence=1.0)
    elif "refund" in text.lower() or "charge" in text.lower():
        return Classification(category=TicketCategory.BILLING, confidence=1.0)
    else:
        return Classification(category=TicketCategory.UNKNOWN, confidence=1.0)

messages = [
    {"role": "system", "content": "You are a helpful assistant that can help with customer support tickets."},
    {"role": "user", "content": "I am extremely frustrated with this service!"}
]

completion = client.beta.chat.completions.parse(
    model="gpt-5-nano",
    messages=messages,
    response_format=Classification
)
result = completion.choices[0].message.parsed

if result.confidence < CONFIDENCE_THRESHOLD:
    print(f"Low confidence score: {result.confidence:.2f}. LLM system lost! Running keyword fallback...")
    fallback_result = run_keyword_fallback(messages[-1]["content"])
    print(f"Fallback result: {fallback_result.category.value.upper()}")
else:
    print(f"LLM system won! Confidence score: {result.confidence:.2f}. Category: {result.category.value.upper()}")