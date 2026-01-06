"""
AI Data Structures Example - Demonstrating Lists, Dictionaries, Tuples, and Sets

This module shows how different Python data structures are used in AI applications:
    - Lists: Ordered, mutable collections (e.g., conversation history, training batches)
    - Dictionaries: Key-value pairs (e.g., model configurations, feature vectors)
    - Tuples: Immutable, ordered collections (e.g., model coordinates, fixed configurations)
    - Sets: Unordered, unique collections (e.g., unique tokens, vocabulary, feature sets)
"""

from typing import List, Dict, Tuple, Set


# ============================================================================
# 1. LISTS - Ordered, Mutable Collections
# ============================================================================
# Use Case: Conversation history, training batches, token sequences

def demonstrate_lists():
    """Shows how lists are used for sequential AI data."""
    print("=" * 60)
    print("1. LISTS - Sequential, Ordered Data")
    print("=" * 60)
    
    # Conversation history (ordered sequence of messages)
    conversation_history: List[str] = [
        "Hello, how can I help you?",
        "Tell me about machine learning",
        "Machine learning is a subset of AI...",
        "Can you give an example?",
        "Sure! Here's an example..."
    ]
    
    print(f"\nConversation History ({len(conversation_history)} messages):")
    for i, msg in enumerate(conversation_history, 1):
        print(f"  {i}. {msg}")
    
    # Tokenized text (list of words/tokens)
    tokens: List[str] = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    print(f"\nTokenized Text: {tokens}")
    print(f"Total Tokens: {len(tokens)}")
    
    # Training batch (list of feature vectors)
    training_scores: List[float] = [0.85, 0.92, 0.78, 0.95, 0.88]
    average_score = sum(training_scores) / len(training_scores)
    print(f"\nTraining Scores: {training_scores}")
    print(f"Average Score: {average_score:.2f}")
    
    # Lists are mutable - you can modify them
    conversation_history.append("Thank you for the explanation!")
    print(f"\nAfter adding message: {len(conversation_history)} total messages")
    print()


# ============================================================================
# 2. DICTIONARIES - Key-Value Pairs
# ============================================================================
# Use Case: Model configurations, embeddings, feature mappings

def demonstrate_dictionaries():
    """Shows how dictionaries store structured AI data."""
    print("=" * 60)
    print("2. DICTIONARIES - Key-Value Structured Data")
    print("=" * 60)
    
    # Model configuration
    model_config: Dict[str, any] = {
        "model_name": "GPT-4",
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.9,
        "system_prompt": "You are a helpful AI assistant."
    }
    
    print("\nModel Configuration:")
    for key, value in model_config.items():
        print(f"  {key}: {value}")
    
    # Word embeddings (word -> vector representation)
    word_embeddings: Dict[str, List[float]] = {
        "python": [0.2, 0.5, 0.1, 0.8],
        "ai": [0.9, 0.3, 0.7, 0.2],
        "machine_learning": [0.6, 0.4, 0.9, 0.5]
    }
    
    print("\nWord Embeddings (sample vectors):")
    for word, vector in word_embeddings.items():
        print(f"  {word}: {vector}")
    
    # Feature mapping (input -> processed output)
    feature_map: Dict[str, int] = {
        "num_words": 150,
        "num_sentences": 8,
        "avg_word_length": 5,
        "sentiment_score": 0.75
    }
    
    print("\nDocument Features:")
    for feature, value in feature_map.items():
        print(f"  {feature}: {value}")
    print()


# ============================================================================
# 3. TUPLES - Immutable, Ordered Collections
# ============================================================================
# Use Case: Fixed configurations, coordinates, immutable data

def demonstrate_tuples():
    """Shows how tuples represent fixed, immutable AI data."""
    print("=" * 60)
    print("3. TUPLES - Immutable, Fixed Data")
    print("=" * 60)
    
    # Model hyperparameters (fixed configuration that shouldn't change)
    hyperparameters: Tuple[int, float, int] = (128, 0.001, 50)  # (batch_size, learning_rate, epochs)
    batch_size, learning_rate, epochs = hyperparameters
    
    print(f"\nHyperparameters (batch_size, learning_rate, epochs): {hyperparameters}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Learning Rate: {learning_rate}")
    print(f"  Epochs: {epochs}")
    
    # Image dimensions (width, height, channels) - immutable
    image_shape: Tuple[int, int, int] = (224, 224, 3)
    width, height, channels = image_shape
    print(f"\nImage Shape (width, height, channels): {image_shape}")
    print(f"  Resolution: {width}x{height}, Channels: {channels}")
    
    # Model coordinates (can be used as dictionary keys unlike lists)
    model_versions: Dict[Tuple[str, int], str] = {
        ("GPT", 3): "Released in 2020",
        ("GPT", 4): "Released in 2023",
        ("BERT", 1): "Released in 2018"
    }
    
    print("\nModel Versions (using tuples as keys):")
    for (model, version), release_info in model_versions.items():
        print(f"  {model} v{version}: {release_info}")
    print()


# ============================================================================
# 4. SETS - Unordered, Unique Collections
# ============================================================================
# Use Case: Vocabulary, unique tokens, removing duplicates

def demonstrate_sets():
    """Shows how sets handle unique, unordered AI data."""
    print("=" * 60)
    print("4. SETS - Unique, Unordered Collections")
    print("=" * 60)
    
    # Vocabulary (unique words from a corpus)
    all_tokens: List[str] = ["the", "cat", "sat", "on", "the", "mat", "the", "cat", "slept"]
    vocabulary: Set[str] = set(all_tokens)
    
    print(f"\nOriginal Tokens: {all_tokens}")
    print(f"Vocabulary (unique tokens): {vocabulary}")
    print(f"Original count: {len(all_tokens)}, Unique count: {len(vocabulary)}")
    
    # Stop words (words to filter out)
    stop_words: Set[str] = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to"}
    filtered_vocab = vocabulary - stop_words
    print(f"\nStop Words: {stop_words}")
    print(f"Filtered Vocabulary (without stop words): {filtered_vocab}")
    
    # Common features across models (set intersection)
    model_a_features: Set[str] = {"neural_network", "backpropagation", "gradient_descent", "optimizer"}
    model_b_features: Set[str] = {"neural_network", "attention", "transformer", "optimizer"}
    common_features = model_a_features & model_b_features  # Intersection
    
    print("\nModel A Features:", model_a_features)
    print("Model B Features:", model_b_features)
    print("Common Features (intersection):", common_features)
    
    # All unique features (set union)
    all_features = model_a_features | model_b_features  # Union
    print("All Features (union):", all_features)
    print()


# ============================================================================
# 5. COMBINING DATA STRUCTURES - Real AI Use Case
# ============================================================================

def demonstrate_combined_structures():
    """Shows a practical example combining all data structures."""
    print("=" * 60)
    print("5. COMBINING DATA STRUCTURES - Real AI Example")
    print("=" * 60)
    
    # List of dictionaries (common in AI APIs and datasets)
    training_examples: List[Dict[str, any]] = [
        {"input": "What is AI?", "output": "AI is artificial intelligence", "confidence": 0.95},
        {"input": "Explain ML", "output": "ML is machine learning", "confidence": 0.88},
        {"input": "What is AI?", "output": "AI is artificial intelligence", "confidence": 0.95}
    ]
    
    print("\nTraining Examples:")
    for i, example in enumerate(training_examples, 1):
        print(f"  Example {i}: {example}")
    
    # Extract unique inputs using set
    unique_inputs: Set[str] = {ex["input"] for ex in training_examples}
    print(f"\nUnique Inputs: {unique_inputs}")
    
    # Calculate average confidence (tuple unpacking)
    confidences: List[float] = [ex["confidence"] for ex in training_examples]
    avg_conf = sum(confidences) / len(confidences)
    conf_tuple: Tuple[float, float] = (min(confidences), max(confidences))
    
    print(f"\nConfidence Statistics:")
    print(f"  Average: {avg_conf:.2f}")
    print(f"  Range (min, max): {conf_tuple}")
    
    # Model registry (dict with tuple keys)
    model_registry: Dict[Tuple[str, str], Dict[str, any]] = {
        ("NLP", "GPT-4"): {"params": 175_000_000_000, "status": "active"},
        ("CV", "ResNet-50"): {"params": 25_000_000, "status": "active"},
        ("NLP", "BERT"): {"params": 110_000_000, "status": "archived"}
    }
    
    print("\nModel Registry (category, model_name) -> details:")
    for (category, model), details in model_registry.items():
        print(f"  {category}/{model}: {details}")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AI DATA STRUCTURES DEMONSTRATION")
    print("=" * 60 + "\n")
    
    demonstrate_lists()
    demonstrate_dictionaries()
    demonstrate_tuples()
    demonstrate_sets()
    demonstrate_combined_structures()
    
    print("=" * 60)
    print("Demonstration Complete!")
    print("=" * 60 + "\n")

