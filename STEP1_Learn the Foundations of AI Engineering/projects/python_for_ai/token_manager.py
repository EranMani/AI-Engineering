"""
Token Management Module - Modular Component #2

This module handles token counting and cost estimation.
By separating token logic, we can:
    - Update token counting algorithms without touching other code
    - Reuse cost estimation across different API integrations
    - Test token calculations independently
    - Swap between different token counting methods
"""

from typing import Dict, List


def count_tokens_simple(text: str) -> int:
    """
    Simple token estimation (1 token ~= 4 characters).
    
    Why modular? Different AI providers use different tokenization.
    This module lets us swap implementations without changing code
    that uses token counting.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def count_tokens_by_words(text: str) -> int:
    """
    Token count based on word splitting (alternative method).
    
    This demonstrates modularity - we can have multiple implementations
    and swap between them without changing calling code.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count based on words
    """
    words = text.split()
    # Rough estimate: 1.3 tokens per word (accounts for punctuation, etc.)
    return int(len(words) * 1.3)


def estimate_cost(tokens: int, cost_per_1k_tokens: float = 0.002) -> float:
    """
    Estimates API cost based on token count.
    
    Why modular? Pricing changes frequently. By isolating this logic,
    we update costs in one place and all code benefits.
    
    Args:
        tokens: Number of tokens
        cost_per_1k_tokens: Cost per 1000 tokens (default: $0.002)
        
    Returns:
        Estimated cost in dollars
    """
    return (tokens / 1000) * cost_per_1k_tokens


def get_token_info(text: str, method: str = "simple") -> Dict[str, any]:
    """
    Comprehensive token information.
    
    This function combines multiple modular operations to provide
    complete token-related metadata.
    
    Args:
        text: Input text
        method: Counting method ("simple" or "words")
        
    Returns:
        Dictionary with token information and cost estimates
    """
    if method == "words":
        token_count = count_tokens_by_words(text)
    else:
        token_count = count_tokens_simple(text)
    
    cost = estimate_cost(token_count)
    
    return {
        "text_length": len(text),
        "token_count": token_count,
        "estimated_cost": cost,
        "method": method
    }

