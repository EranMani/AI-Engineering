"""
Lesson 1: Basic LLM Usage with LangChain
==========================================

In this lesson, you'll learn:
1. How to set up LangChain with OpenAI
2. How to make your first LLM call
3. Understanding the basic components: LLM vs ChatModel
4. Production best practices: error handling and API key management

Key Concepts:
- LLM: Language Model (text-in, text-out)
- ChatModel: Chat Model (messages-in, messages-out) - More structured, preferred for production
- Environment variables: Never hardcode API keys
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()


def lesson_01_basic_usage():
    """
    Basic usage: Making your first LLM call
    
    Production Tip: Always use ChatOpenAI instead of OpenAI (deprecated)
    ChatOpenAI uses the ChatModel interface which is more structured and reliable.
    """
    print("=" * 60)
    print("LESSON 1: Basic LLM Usage")
    print("=" * 60)
    
    # Step 1: Initialize the model
    # Production Tip: Always specify temperature and model explicitly
    # Temperature: 0 = deterministic, 1 = creative (use 0.7 for most cases)
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Explicit model selection
        temperature=0.7,       # Control randomness
        api_key=os.getenv("OPENAI_API_KEY")  # From environment
    )
    
    # Step 2: Create a simple message
    # ChatModel uses messages (more structured than plain text)
    message = HumanMessage(content="What is LangChain in one sentence?")
    
    # Step 3: Invoke the model
    response = llm.invoke([message])
    
    # Step 4: Extract the response
    print(f"\nQuestion: {message.content}")
    print(f"Answer: {response.content}\n")
    
    return response


def lesson_01_with_system_message():
    """
    Using System Messages for better control
    
    System messages help set the behavior and context for the AI.
    This is a production pattern you'll use everywhere.
    """
    print("=" * 60)
    print("LESSON 1: Using System Messages")
    print("=" * 60)
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # System message sets the role/behavior
    system_msg = SystemMessage(
        content="You are a helpful AI assistant specialized in explaining "
                "complex concepts in simple terms."
    )
    
    # Human message is the user's question
    human_msg = HumanMessage(
        content="Explain what a vector database is."
    )
    
    # Invoke with both messages
    response = llm.invoke([system_msg, human_msg])
    
    print(f"\nSystem Role: {system_msg.content}")
    print(f"Question: {human_msg.content}")
    print(f"Answer: {response.content}\n")
    
    return response


def lesson_01_error_handling():
    """
    Production Pattern: Error Handling
    
    Always wrap LLM calls in try-except blocks.
    Common errors: API key issues, rate limits, network problems.
    """
    print("=" * 60)
    print("LESSON 1: Error Handling (Production Pattern)")
    print("=" * 60)
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    try:
        message = HumanMessage(content="Hello!")
        response = llm.invoke([message])
        print(f"Success: {response.content}\n")
        return response
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}\n")
        # In production, you'd log this and handle gracefully
        raise


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found in environment!")
        print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
        exit(1)
    
    # Run lessons
    lesson_01_basic_usage()
    lesson_01_with_system_message()
    lesson_01_error_handling()
    
    print("✅ Lesson 1 Complete!")
    print("\n📝 Key Takeaways:")
    print("  1. Always use ChatOpenAI (not OpenAI)")
    print("  2. Use SystemMessage for role/context")
    print("  3. Always handle errors")
    print("  4. Never hardcode API keys")
