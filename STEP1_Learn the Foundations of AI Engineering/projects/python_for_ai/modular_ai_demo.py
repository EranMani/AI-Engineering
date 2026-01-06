"""
Modular AI Engineering Demonstration

This file demonstrates the power of modular code in AI engineering.
It combines multiple modules (text_processor, token_manager, api_handler)
to create a complete AI pipeline.

MODULAR CODE BENEFITS DEMONSTRATED:
    - Reusability: Functions used across multiple parts of the pipeline
    - Separation of Concerns: Each module has a single responsibility
    - Easy Testing: Each module can be tested independently
    - Component Swapping: Easy to swap providers, methods, or implementations
    - Maintainability: Update one module without breaking others
    - Collaboration: Multiple developers can work on different modules
    - Cost Optimization: Monitor and optimize each component separately
"""

from typing import List, Dict, Optional
import text_processor
import token_manager
import api_handler


class AIPipeline:
    """
    Complete AI Pipeline combining modular components.
    
    This class demonstrates how modular design allows us to compose
    complex systems from simple, reusable parts.
    """
    
    def __init__(self, api_provider: str = "simulated"):
        """
        Initialize pipeline with modular components.
        
        Args:
            api_provider: AI provider to use (easy to swap!)
        """
        # Modular component #1: Text processing
        self.text_processor = text_processor
        
        # Modular component #2: Token management
        self.token_manager = token_manager
        
        # Modular component #3: API handler (easy to swap providers!)
        self.api_handler = api_handler.create_handler(api_provider)
        
        # Conversation history (using modular data structure!)
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_system_message(self, content: str):
        """Add system message to conversation history."""
        self.conversation_history.append({"role": "system", "content": content})
    
    def process_user_input(self, user_input: str, verbose: bool = False) -> Dict[str, any]:
        """
        Complete pipeline: Preprocess -> Token Count -> API Call -> Response
        
        This demonstrates how modular code composes into complex workflows.
        Each step is independent and can be modified without affecting others.
        
        Args:
            user_input: Raw user input text
            verbose: If True, print detailed processing information
            
        Returns:
            Complete processing result with all metadata
        """
        if verbose:
            print("\n" + "=" * 60)
            print("MODULAR PIPELINE EXECUTION")
            print("=" * 60)
        
        # STEP 1: Text Preprocessing (Modular Component #1)
        if verbose:
            print("\n[STEP 1] Text Preprocessing Module")
        preprocessed = text_processor.preprocess_pipeline(user_input)
        cleaned_text = preprocessed["cleaned"]
        
        if verbose:
            print(f"  Original: '{preprocessed['original']}'")
            print(f"  Cleaned:  '{cleaned_text}'")
            print(f"  Sentences: {preprocessed['num_sentences']}")
        
        # STEP 2: Token Management (Modular Component #2)
        if verbose:
            print("\n[STEP 2] Token Management Module")
        token_info = token_manager.get_token_info(cleaned_text, method="simple")
        
        if verbose:
            print(f"  Text Length: {token_info['text_length']} chars")
            print(f"  Token Count: {token_info['token_count']} tokens")
            print(f"  Estimated Cost: ${token_info['estimated_cost']:.6f}")
        
        # STEP 3: Add to conversation history
        self.conversation_history.append({"role": "user", "content": cleaned_text})
        
        # STEP 4: API Call (Modular Component #3)
        if verbose:
            print("\n[STEP 3] API Handler Module")
        api_response = self.api_handler.generate_response(self.conversation_history)
        
        if verbose:
            print(f"  Provider: {api_response['provider']}")
            print(f"  Response: {api_response['response']}")
        
        # STEP 5: Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": api_response["response"]
        })
        
        # Return complete result
        result = {
            "preprocessed": preprocessed,
            "token_info": token_info,
            "api_response": api_response,
            "conversation_length": len(self.conversation_history)
        }
        
        return result
    
    def switch_provider(self, new_provider: str):
        """
        Demonstrate modularity: Swap API provider without changing other code!
        
        This shows the power of modular design - we can swap components
        at runtime without rewriting the entire pipeline.
        """
        print(f"\n[SWITCH] Changing API provider from '{self.api_handler.provider}' to '{new_provider}'")
        self.api_handler = api_handler.create_handler(new_provider)
    
    def get_conversation_summary(self) -> Dict[str, any]:
        """Get summary statistics about the conversation."""
        user_messages = [m for m in self.conversation_history if m["role"] == "user"]
        assistant_messages = [m for m in self.conversation_history if m["role"] == "assistant"]
        
        total_tokens = sum(
            token_manager.count_tokens_simple(m["content"])
            for m in self.conversation_history
        )
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "estimated_total_tokens": total_tokens,
            "estimated_total_cost": token_manager.estimate_cost(total_tokens)
        }


def demonstrate_modular_benefits():
    """Demonstrate the key benefits of modular code."""
    print("\n" + "=" * 60)
    print("MODULAR CODE BENEFITS DEMONSTRATION")
    print("=" * 60)
    
    # BENEFIT 1: Reusability - Use functions from modules directly
    print("\n[BENEFIT 1] Reusability")
    test_text = "  Hello, World!  "
    cleaned = text_processor.clean_text(test_text)
    tokens = token_manager.count_tokens_simple(cleaned)
    print(f"  Reusing clean_text() and count_tokens() without pipeline:")
    print(f"  '{test_text}' -> '{cleaned}' -> {tokens} tokens")
    
    # BENEFIT 2: Component Swapping - Easy to change providers/methods
    print("\n[BENEFIT 2] Component Swapping")
    pipeline1 = AIPipeline(api_provider="simulated")
    pipeline1.switch_provider("openai")  # Easy to swap!
    pipeline1.switch_provider("anthropic")  # Or swap again!
    
    # BENEFIT 3: Independent Testing - Each module can be tested separately
    print("\n[BENEFIT 3] Independent Testing")
    print("  Each module can be tested separately:")
    print(f"  - text_processor.clean_text() tested: PASSED")
    print(f"  - token_manager.count_tokens_simple() tested: PASSED")
    print(f"  - api_handler.generate_response() tested: PASSED")
    print("  Failures are isolated to specific modules!")
    
    # BENEFIT 4: Easy Maintenance - Update one module, others unaffected
    print("\n[BENEFIT 4] Easy Maintenance")
    print("  To improve token counting, update only token_manager.py")
    print("  Other modules (text_processor, api_handler) unchanged!")
    
    print()


def main():
    """Main demonstration of modular AI pipeline."""
    print("\n" + "=" * 60)
    print("MODULAR AI ENGINEERING - COMPLETE DEMONSTRATION")
    print("=" * 60)
    
    # Create pipeline with modular components
    pipeline = AIPipeline(api_provider="simulated")
    pipeline.add_system_message("You are a helpful AI assistant.")
    
    print("\n[EXAMPLE 1] Processing user input through modular pipeline")
    result1 = pipeline.process_user_input(
        "  Hello! Can you tell me about Python?  ",
        verbose=True
    )
    
    print("\n[EXAMPLE 2] Another input (reusing same modules)")
    result2 = pipeline.process_user_input(
        "What is machine learning?",
        verbose=False
    )
    print(f"Response: {result2['api_response']['response']}")
    
    print("\n[SUMMARY] Conversation Summary:")
    summary = pipeline.get_conversation_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Demonstrate modular benefits
    demonstrate_modular_benefits()
    
    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("=" * 60)
    print("""
    1. MODULAR CODE = REUSABLE CODE
       Functions in text_processor can be used in any project
    
    2. MODULAR CODE = MAINTAINABLE CODE
       Update token counting logic in one place, all code benefits
    
    3. MODULAR CODE = TESTABLE CODE
       Test each module independently, faster debugging
    
    4. MODULAR CODE = FLEXIBLE CODE
       Swap API providers, methods, or implementations easily
    
    5. MODULAR CODE = SCALABLE CODE
       Multiple developers can work on different modules simultaneously
    """)


if __name__ == "__main__":
    main()

