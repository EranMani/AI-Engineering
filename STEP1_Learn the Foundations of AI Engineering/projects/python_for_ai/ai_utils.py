# ai_utils.py
# This file contains reusable tools, but DOES NOT run any code itself.

"""
In programming and data science, raw text from users or files is often "messy." 
It might contain inconsistent capitalization, extra spaces, or weird symbols.
"""

def clean_text(text: str) -> str:
    """Removes extra spaces and makes text lowercase for processing."""
    return text.strip().lower()

def count_tokens_simple(text: str) -> int:
    """A rough estimate of token count (1 token ~= 4 chars)."""
    return len(text) // 4