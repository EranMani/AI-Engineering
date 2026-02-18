"""
Example: PydanticAI Agent with Local Ollama Models

Purpose: Run AI agents locally with Ollama—no API key, no token costs.
Concepts: OllamaProvider, OpenAIChatModel, model switching (local vs cloud)
Level: Reference

Prerequisites:
  1. Install Ollama: https://ollama.com
  2. Pull a model: ollama pull llama3.2
  3. Run Ollama (it starts automatically after install, or: ollama serve)
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider


# =============================================================================
# OUTPUT SCHEMA
# =============================================================================

class MovieResult(BaseModel):
    """Structured output—same as with OpenAI."""
    title: str = Field(description="The movie title")
    year: int = Field(description="Release year")
    director: str = Field(description="The director's name")


# =============================================================================
# APPROACH 1: Shorthand with ollama: prefix (uses OLLAMA_BASE_URL env var)
# =============================================================================

def run_with_shorthand():
    """Simplest: Agent('ollama:llama3.2'). Set OLLAMA_BASE_URL if not localhost."""
    agent = Agent("ollama:llama3.2", output_type=MovieResult)
    result = agent.run_sync("What is the best movie of all time?")
    print("Shorthand result:", result.output)


# =============================================================================
# APPROACH 2: Explicit OllamaProvider (no env vars needed)
# =============================================================================

def run_with_explicit_provider():
    """Explicit config. Use this when you want full control or a remote Ollama."""
    ollama_model = OpenAIChatModel(
        model_name="llama3.2",  # or mistral, gemma2, phi3, etc.
        provider=OllamaProvider(base_url="http://localhost:11434/v1"),
    )
    agent = Agent(ollama_model, output_type=MovieResult)
    result = agent.run_sync("Tell me about Inception")
    print("Explicit result:", result.output)


# =============================================================================
# APPROACH 3: Simple chat (no structured output)
# =============================================================================

def run_simple_chat():
    """Plain text response—good for quick testing."""
    agent = Agent(
        OpenAIChatModel(
            model_name="llama3.2",
            provider=OllamaProvider(base_url="http://localhost:11434/v1"),
        ),
        result_type=str,
    )
    result = agent.run_sync("What is 2 + 2? Reply with just the number.")
    print("Simple chat:", result.output)


# =============================================================================
# VANILLA OPENAI CLIENT + OLLAMA (no PydanticAI)
# =============================================================================

def run_vanilla_ollama():
    """Using plain OpenAI client—Ollama exposes OpenAI-compatible API."""
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Placeholder; Ollama ignores it for local
    )
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": "What is 25 + 17? Reply with just the number."}],
    )
    print("Vanilla Ollama:", response.choices[0].message.content)


# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Ollama + PydanticAI Example")
    print("Prerequisites: ollama pull llama3.2")
    print("=" * 60)

    try:
        # Uncomment the one you want to run:
        # run_with_shorthand()
        run_with_explicit_provider()
        # run_simple_chat()
        # run_vanilla_ollama()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Ollama is running:")
        print("  1. Install from https://ollama.com")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Ollama serves at http://localhost:11434")
