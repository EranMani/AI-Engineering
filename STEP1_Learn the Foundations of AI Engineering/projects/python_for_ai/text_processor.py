"""
Text Processing Module - Modular Component #1

This module handles text cleaning and preprocessing operations.
By separating this into its own module, we can:
    - Reuse text cleaning across multiple projects
    - Test preprocessing logic independently
    - Swap different preprocessing strategies easily
    - Update text processing without affecting other code
"""

from typing import List


def clean_text(text: str) -> str:
    """
    Removes extra spaces and converts text to lowercase.
    
    Why modular? This function can be used by chatbots, data pipelines,
    and API handlers without duplicating code.
    
    Args:
        text: Raw input text that may have inconsistent formatting
        
    Returns:
        Cleaned text ready for processing
    """
    return text.strip().lower()


def remove_special_chars(text: str, keep_spaces: bool = True) -> str:
    """
    Removes special characters, keeping only alphanumeric and optionally spaces.
    
    Args:
        text: Input text
        keep_spaces: If True, preserves spaces; if False, removes all non-alphanumeric
        
    Returns:
        Text with special characters removed
    """
    if keep_spaces:
        return ''.join(c for c in text if c.isalnum() or c.isspace())
    else:
        return ''.join(c for c in text if c.isalnum())


def split_into_sentences(text: str) -> List[str]:
    """
    Splits text into sentences (simple implementation).
    
    Why modular? Sentence splitting is needed for many NLP tasks.
    By making it a module, we can improve this function without
    breaking code that uses it.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    sentences = text.split('.')
    return [s.strip() for s in sentences if s.strip()]


def preprocess_pipeline(text: str) -> dict:
    """
    Complete preprocessing pipeline combining multiple steps.
    
    This demonstrates composition of modular functions - combining
    smaller modules into a larger workflow.
    
    Args:
        text: Raw input text
        
    Returns:
        Dictionary with processed text and metadata
    """
    cleaned = clean_text(text)
    sentences = split_into_sentences(cleaned)
    
    return {
        "original": text,
        "cleaned": cleaned,
        "sentences": sentences,
        "num_sentences": len(sentences)
    }

