"""
API Handler Module - Modular Component #3

This module simulates AI API interactions.
By separating API logic, we can:
    - Swap between different AI providers (OpenAI, Anthropic, local models)
    - Test API calls without making real requests
    - Update API integration without affecting preprocessing
    - Implement A/B testing between different providers
"""

from typing import Dict, List, Optional


class APIHandler:
    """
    Base handler for AI API interactions.
    
    Why a class? It allows us to configure API settings once
    and reuse them across multiple calls. This is modular design
    at the object level.
    """
    
    def __init__(self, provider: str = "simulated", api_key: Optional[str] = None):
        """
        Initialize API handler with provider configuration.
        
        Args:
            provider: AI provider name ("simulated", "openai", "anthropic")
            api_key: API key (not used in simulation)
        """
        self.provider = provider
        self.api_key = api_key
        self.call_count = 0
    
    def format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Formats messages for API consumption.
        
        Different providers may need different formats. By making
        this modular, we can adapt to provider requirements easily.
        
        Args:
            messages: List of message dictionaries with "role" and "content"
            
        Returns:
            Formatted messages ready for API
        """
        # Standard OpenAI/Anthropic format
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        return formatted
    
    def simulate_call(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Simulates an API call (for demonstration).
        
        In production, this would make real API calls. The modular
        design means we can swap this implementation without changing
        code that uses it.
        
        Args:
            messages: Formatted messages
            
        Returns:
            Simulated API response
        """
        self.call_count += 1
        user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        # Simulate response based on input
        if "hello" in user_message.lower():
            response = "Hello! How can I assist you today?"
        elif "python" in user_message.lower():
            response = "Python is a versatile programming language used extensively in AI."
        else:
            response = f"Simulated response to: {user_message[:50]}..."
        
        return {
            "response": response,
            "provider": self.provider,
            "call_number": self.call_count,
            "messages_processed": len(messages)
        }
    
    def generate_response(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Main method to generate AI responses.
        
        This is the public interface. Internal implementation can change
        (real API, different provider) without affecting calling code.
        
        Args:
            messages: Conversation history
            
        Returns:
            API response with generated text
        """
        formatted = self.format_messages(messages)
        return self.simulate_call(formatted)


def create_handler(provider: str) -> APIHandler:
    """
    Factory function to create appropriate handler.
    
    Why modular? We can easily add new providers or swap implementations.
    The calling code doesn't need to know how handlers are created.
    
    Args:
        provider: Provider name
        
    Returns:
        Configured APIHandler instance
    """
    return APIHandler(provider=provider)

