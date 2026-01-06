"""
This module demonstrates several fundamental Python concepts:

Concepts Demonstrated:
    - Type Hints: Using typing module (List, Dict) for static type annotations
    - Lists: Ordered collections of items (conversation_history)
    - Dictionaries: Key-value pairs for structured data (message objects)
    - Type Annotations: Function parameters and return types (List[Dict[str, str]], -> None)
    - F-strings: Formatted string literals for string interpolation
    - Function Definitions: Defining reusable code blocks with parameters
    - For Loops: Iterating over iterable collections (lists)
    - Conditional Statements: if/elif/else for control flow based on conditions
    - String Methods: Using .upper() to transform string case
    - Dictionary Access: Using bracket notation to access dictionary values by key
    - Built-in Functions: Using len() to get the length of a collection
"""

# A Type Hint for a more complex structure (List of Dictionaries)
from typing import List, Dict

# 1. The Data: A conversation history (List of Dictionaries)
conversation_history: List[Dict[str, str]] = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Explain quantum physics like I'm five."},
    {"role": "assistant", "content": "Imagine throwing a ball at a wall..."}
]

# 2. The Function: Processing the data
def format_chat_log(messages: List[Dict[str, str]]) -> None:
    """
    Iterates through a list of message dictionaries and prints them nicely.
    """
    print(f"--- Processing {len(messages)} Messages ---")
    
    for msg in messages:
        # Extracting values from the Dictionary keys
        role = msg["role"].upper()
        content = msg["content"]
        
        # Logic: formatting based on role
        if role == "SYSTEM":
            print(f"⚙️ [{role}]: {content}")
        elif role == "USER":
            print(f"👤 [{role}]: {content}")
        else:
            print(f"🤖 [{role}]: {content}")

# 3. Execution
format_chat_log(conversation_history)