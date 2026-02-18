"""
LangChain Learning Hub
======================

Welcome! This is your learning journey from zero to hero with LangChain.

Run individual lessons:
    python lesson_01_basic_llm.py
    python lesson_02_prompt_templates.py  (coming soon)
    ...

Or use this main file to navigate through lessons.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_setup():
    """Verify that the environment is set up correctly."""
    print("🔍 Checking setup...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        print("📝 Please create a .env file with your API key.")
        print("   Example: OPENAI_API_KEY=sk-your-key-here")
        return False
    
    print("✅ API key found!")
    return True


def show_menu():
    """Display the learning menu."""
    print("\n" + "=" * 60)
    print("LangChain: From Zero to Hero 🚀")
    print("=" * 60)
    print("\nAvailable Lessons:")
    print("  1. Lesson 1: Basic LLM Usage")
    print("  2. Lesson 2: Prompt Templates (Coming Soon)")
    print("  3. Lesson 3: Chains (Coming Soon)")
    print("  4. Lesson 4: Memory (Coming Soon)")
    print("  5. Lesson 5: RAG Basics (Coming Soon)")
    print("\n  0. Exit")
    print("\n" + "=" * 60)


def main():
    """Main entry point for the learning hub."""
    if not check_setup():
        return
    
    show_menu()
    
    choice = input("\nSelect a lesson (1-5) or 0 to exit: ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Lesson 1...\n")
        from lesson_01_basic_llm import (
            lesson_01_basic_usage,
            lesson_01_with_system_message,
            lesson_01_error_handling
        )
        lesson_01_basic_usage()
        lesson_01_with_system_message()
        lesson_01_error_handling()
        print("\n✅ Lesson 1 Complete!")
        print("📚 Check LANGCHAIN_GUIDE.md for detailed explanations.")
    elif choice == "0":
        print("👋 Goodbye! Keep learning!")
    else:
        print("⚠️  Lesson not available yet. Check back soon!")


if __name__ == "__main__":
    main()
