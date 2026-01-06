"""
LIST PRACTICE EXERCISES
Complete each exercise by writing code in the designated sections.
Each exercise focuses on a key list concept for AI engineering.
"""

from itertools import accumulate
from re import split


print("=" * 60)
print("LIST PRACTICE EXERCISES")
print("=" * 60)

# ============================================================================
# EXERCISE 1: Mastering Slicing [start:end:step]
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 1: Mastering Slicing")
print("=" * 60)

# Scenario: You have tokenized text and need to extract specific portions
tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]

# TODO: Complete the following slicing operations:
# 1. Extract the first 3 tokens
first_three = tokens[:3]

# 2. Extract the last 3 tokens
last_three = tokens[-3:]

# 3. Extract tokens from index 2 to 5 (inclusive of 2, exclusive of 5)
middle_section = tokens[2:5]

# 4. Extract every 2nd token starting from index 0
every_second = tokens[::2]

# 5. Reverse the entire list using slicing
reversed_tokens = tokens[::-1]  # Replace None with your slice

# 6. Extract tokens from index 1 to the end, skipping every 2nd one
skip_pattern = tokens[1::2]

# Expected outputs:
# first_three: ['The', 'quick', 'brown']
# last_three: ['the', 'lazy', 'dog']
# middle_section: ['brown', 'fox', 'jumps']
# every_second: ['The', 'brown', 'jumps', 'the', 'dog']
# reversed_tokens: ['dog', 'lazy', 'the', 'over', 'jumps', 'fox', 'brown', 'quick', 'The']
# skip_pattern: ['quick', 'fox', 'over', 'lazy']

print(f"First three: {first_three}")
print(f"Last three: {last_three}")
print(f"Middle section: {middle_section}")
print(f"Every second: {every_second}")
print(f"Reversed: {reversed_tokens}")
print(f"Skip pattern: {skip_pattern}")


# ============================================================================
# EXERCISE 2: List Comprehensions (Pythonic and Fast)
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 2: List Comprehensions")
print("=" * 60)

# Scenario: Processing AI model confidence scores and token data
raw_scores = [0.45, 0.92, 0.67, 0.33, 0.88, 0.15]
tokens_lower = ["the", "cat", "sat", "on", "the", "mat"]

# TODO: Use list comprehensions to:
# 1. Square each score (transform each element)
squared_scores = [score**2 for score in raw_scores]

# 2. Filter scores that are >= 0.5 (conditional filtering)
high_confidence = [score for score in raw_scores if score >= 0.5]

# 3. Create a list of score strings formatted as "Score: 0.XX"
formatted_scores = [f"Score: {score:.2f}" for score in raw_scores]

# 4. Get lengths of each token
token_lengths = [len(token) for token in tokens_lower]

# 5. Create tuples of (token, length) for tokens longer than 3 characters
long_tokens_info = [(token, len(token)) for token in tokens_lower if len(token) > 3]

# Expected outputs:
# squared_scores: [0.2025, 0.8464, 0.4489, 0.1089, 0.7744, 0.0225]
# high_confidence: [0.92, 0.67, 0.88]
# formatted_scores: ['Score: 0.45', 'Score: 0.92', 'Score: 0.67', 'Score: 0.33', 'Score: 0.88', 'Score: 0.15']
# token_lengths: [3, 3, 3, 2, 3, 3]
# long_tokens_info: []  (all tokens are 3 chars or less)

print(f"Squared scores: {squared_scores}")
print(f"High confidence: {high_confidence}")
print(f"Formatted scores: {formatted_scores}")
print(f"Token lengths: {token_lengths}")
print(f"Long tokens info: {long_tokens_info}")


# ============================================================================
# EXERCISE 3: append() vs extend() vs insert()
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 3: append() vs extend() vs insert()")
print("=" * 60)

# Scenario: Building conversation history for an AI chatbot
conversation = []

# TODO: Complete the following operations:
# 1. Add a single user message using append()
#    Message: {"role": "user", "content": "Hello, AI!"}
#    Use: conversation.append(...)
conversation.append({"role": "user", "content": "Hello, AI!"})

# 2. Add multiple messages at once using extend()
#    Messages: [{"role": "assistant", "content": "Hi there!"}, {"role": "user", "content": "How are you?"}]
#    Use: conversation.extend(...)
conversation.extend([{"role": "assistant", "content": "Hi there!"}, {"role": "user", "content": "How are you?"}])

# 3. Insert a system message at the beginning (index 0) using insert()
#    Message: {"role": "system", "content": "You are a helpful assistant."}
#    Use: conversation.insert(...)
conversation.insert(0, {"role": "system", "content": "You are a helpful assistant."})

# 4. Add another user message at the end using append()
#    Message: {"role": "user", "content": "Tell me about Python"}
#    Use: conversation.append(...)
conversation.append({"role": "user", "content": "Tell me about Python"})

# Expected final conversation:
# [
#   {"role": "system", "content": "You are a helpful assistant."},
#   {"role": "user", "content": "Hello, AI!"},
#   {"role": "assistant", "content": "Hi there!"},
#   {"role": "user", "content": "How are you?"},
#   {"role": "user", "content": "Tell me about Python"}
# ]

print(f"Final conversation ({len(conversation)} messages):")
for i, msg in enumerate(conversation, 1):
    print(f"  {i}. {msg['role']}: {msg['content']}")


# ============================================================================
# EXERCISE 4: enumerate() and zip() for Loops
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 4: enumerate() and zip()")
print("=" * 60)

# Scenario: Processing training data with features and labels
features = [0.1, 0.5, 0.9, 0.3, 0.7]
labels = ["positive", "negative", "positive", "negative", "positive"]
model_names = ["GPT-3", "GPT-4", "Claude", "BERT", "T5"]

# TODO: Complete the following:
# 1. Use enumerate() to print each feature with its index
#    Format: "Index 0: Feature = 0.1"
print("Using enumerate():")
for i, feat in enumerate(features):
    print(f"Index {i}: Featuer = {feat}")
# Write your loop here using enumerate(features)

# 2. Use zip() to combine features and labels, then print pairs
#    Format: "Feature 0.1 -> Label: positive"
print("\nUsing zip() with features and labels:")
for feat, label in zip(features, labels):
    print(f"Feature {feat} -> Label: {label}")
# Write your loop here using zip(features, labels)

# 3. Use zip() with THREE lists: model_names, features, and labels
#    Format: "GPT-3: Feature=0.1, Label=positive"
print("\nUsing zip() with three lists:")
for model, feat, label in zip(model_names, features, labels):
    print(f"{model}: Feature={feat}, Label={label}")
# Write your loop here using zip(model_names, features, labels)

# 4. Create a list of dictionaries using zip() and list comprehension
#    Each dict should have: {"model": name, "feature": value, "label": label}
combined_data = [f"model: {model}, feature: {feat}, label: {label}" for model, feat, label in zip(model_names, features, labels)]

print(f"\nCombined data: {combined_data}")


# ============================================================================
# EXERCISE 5: sort() vs sorted() - In-place vs New List
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 5: sort() vs sorted()")
print("=" * 60)

# Scenario: Analyzing model performance scores
original_scores = [0.85, 0.92, 0.78, 0.95, 0.88]
model_names = ["GPT-4", "Claude", "GPT-3", "BERT", "T5"]

# TODO: Complete the following:
# 1. Use sorted() to create a NEW sorted list (ascending) without modifying original_scores
#    Store result in: ascending_scores
ascending_scores = sorted(original_scores)

# 2. Use sorted() to create a NEW sorted list (descending) without modifying original_scores
#    Store result in: descending_scores
descending_scores = sorted(original_scores, reverse=True)

# 3. Use sort() to sort original_scores IN PLACE (ascending)
#    This will modify original_scores
#    Use: original_scores.sort()
#original_scores.sort()

# 4. Verify that original_scores was modified but ascending_scores is independent
print(f"Original scores after sort(): {original_scores}")
print(f"Ascending scores (new list): {ascending_scores}")
print(f"Descending scores (new list): {descending_scores}")
print(f"Are they the same object? {original_scores is ascending_scores}")

# 5. BONUS: Sort model_names by the corresponding score (using zip and sorted)
#    Hint: zip model_names with original_scores, sort by score, then extract names
#    Expected: ['GPT-3', 'GPT-4', 'T5', 'Claude', 'BERT'] (sorted by score ascending)
models_by_score = [model for model, score in sorted(zip(model_names, original_scores), key=lambda x: x[1])]

print(f"\nModels sorted by score: {models_by_score}")

print("\n" + "=" * 60)
print("EXERCISES COMPLETE!")
print("=" * 60)


# ============================================================================
# EXERCISE 6: Advanced Data Processing - Nested Lists and Grouping
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 6: Advanced Data Processing - Nested Lists and Grouping")
print("=" * 60)

# Scenario: You're processing multiple AI model inference results
# Each model ran on multiple test cases, and you need to analyze the results

model_results = [
    {"model": "GPT-4", "test_id": 1, "accuracy": 0.92, "latency_ms": 150, "tokens": 1200},
    {"model": "Claude", "test_id": 1, "accuracy": 0.89, "latency_ms": 180, "tokens": 1100},
    {"model": "GPT-4", "test_id": 2, "accuracy": 0.88, "latency_ms": 145, "tokens": 980},
    {"model": "Claude", "test_id": 2, "accuracy": 0.91, "latency_ms": 175, "tokens": 1050},
    {"model": "GPT-3", "test_id": 1, "accuracy": 0.85, "latency_ms": 200, "tokens": 1300},
    {"model": "GPT-3", "test_id": 2, "accuracy": 0.83, "latency_ms": 195, "tokens": 1250},
    {"model": "BERT", "test_id": 1, "accuracy": 0.78, "latency_ms": 50, "tokens": 800},
    {"model": "BERT", "test_id": 2, "accuracy": 0.80, "latency_ms": 55, "tokens": 850},
]

# TODO: Complete the following tasks using list operations:

# 1. Extract all unique model names from the results
#    Expected: ['GPT-4', 'Claude', 'GPT-3', 'BERT']
unique_models = list((set([model["model"] for model in model_results]))).sort()

# 2. Group results by model name, creating a nested list structure
#    Format: {model_name: [list of results for that model]}
#    Hint: Use a dictionary comprehension with filtering
#    Expected structure: {'GPT-4': [result1, result2], 'Claude': [result1, result2], ...}
grouped_by_model = {model["model"]: [result["accuracy"] for result in model_results if result["model"] == model["model"]] for model in model_results}

# 3. Calculate average accuracy for each model
#    Format: List of tuples: [(model_name, avg_accuracy), ...]
#    Expected: [('GPT-4', 0.90), ('Claude', 0.90), ('GPT-3', 0.84), ('BERT', 0.79)]
#    Hint: Use list comprehension, sum(), len(), and the grouped data
model_avg_accuracy = [(model, sum(values)/ len(values)) for model, values in grouped_by_model.items()]

# 4. Find the best performing model for each test_id
#    Format: List of dicts: [{"test_id": 1, "best_model": "GPT-4", "accuracy": 0.92}, ...]
#    Expected: [{"test_id": 1, "best_model": "GPT-4", "accuracy": 0.92}, 
#               {"test_id": 2, "best_model": "Claude", "accuracy": 0.91}]
#    Hint: Group by test_id first, then find max accuracy
unique_test_ids = set(result["test_id"] for result in model_results)
groupded_by_test_id = {test_id: [result for result in model_results if result["test_id"] == test_id] for test_id in unique_test_ids}
best_per_test = [{"test_id": test_id, 
                  "best_model": max(results, key=lambda x: x["accuracy"])["model"],
                  "accuracy": max(results, key=lambda x: x["accuracy"])["accuracy"]} for test_id, results in groupded_by_test_id.items()]


# 5. Create a ranking of models by average accuracy (descending)
#    Format: List of tuples: [(rank, model_name, avg_accuracy), ...]
#    Expected: [(1, 'GPT-4', 0.90), (1, 'Claude', 0.90), (3, 'GPT-3', 0.84), (4, 'BERT', 0.79)]
#    Note: GPT-4 and Claude tie for rank 1, so both get rank 1
#    Hint: Sort by accuracy, then assign ranks (handling ties)
unique_models = set(result["model"] for result in model_results)
group_by_accuracy = {model: [result["accuracy"] for result in model_results if result["model"] == model] for model in unique_models}
model_avg_acc = {model: sum(accuracies) / len(accuracies) for model, accuracies in group_by_accuracy.items()}
sorted_models = sorted([(model, avg_acc) for model, avg_acc in model_avg_acc.items()], key=lambda x: x[1], reverse=True)

current_rank = 1
model_rankings = []

for i, (model, avg_acc) in enumerate(sorted_models):
    if i > 0 and sorted_models[i-1][1] != avg_acc:
        current_rank = i + 1

    model_rankings.append((current_rank, model, avg_acc))

# 6. Filter models that have BOTH accuracy >= 0.85 AND latency < 200ms
#    Format: List of model names (unique)
#    Expected: ['GPT-4', 'Claude']
#    Hint: Check all results for each model
unique_models = set(result["model"] for result in model_results)
high_performance_models = [model for model in unique_models if all(
    r["accuracy"] >= 0.85 and r["latency_ms"] < 200
    for r in model_results if r["model"] == model
)]

print(f"Unique models: {unique_models}")
print(f"\nGrouped by model: {list(grouped_by_model.keys()) if grouped_by_model else None}")
print(f"Model average accuracy: {model_avg_accuracy}")
print(f"Best per test: {best_per_test}")
print(f"Model rankings: {model_rankings}")
print(f"High performance models: {high_performance_models}")


# ============================================================================
# EXERCISE 7: Advanced List Manipulation - Sliding Windows and Chunking
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 7: Advanced List Manipulation - Sliding Windows and Chunking")
print("=" * 60)

# Scenario: Processing tokenized text for n-gram analysis and batch processing
tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "and", "runs", "fast"]
scores = [0.95, 0.88, 0.92, 0.85, 0.90, 0.87, 0.93, 0.89, 0.91, 0.86, 0.94, 0.88]

# TODO: Complete the following advanced operations:

# 1. Create bigrams (2-word sequences) using a sliding window
#    Format: List of tuples: [("The", "quick"), ("quick", "brown"), ...]
#    Expected: [("The", "quick"), ("quick", "brown"), ("brown", "fox"), ...]
#    Hint: Use list comprehension with enumerate and slicing
bigrams = [(tokens[i], tokens[i+1]) for i, _ in enumerate(tokens[:-1])]

# 2. Create trigrams (3-word sequences) using a sliding window
#    Format: List of tuples: [("The", "quick", "brown"), ("quick", "brown", "fox"), ...]
trigrams = [(tokens[i], tokens[i+1], tokens[i+2]) for i, _ in enumerate(tokens[:-2])]

# 3. Chunk the tokens list into batches of size 4
#    Format: List of lists: [["The", "quick", "brown", "fox"], ["jumps", "over", "the", "lazy"], ...]
#    Expected: [["The", "quick", "brown", "fox"], ["jumps", "over", "the", "lazy"], ["dog", "and", "runs", "fast"]]
#    Hint: Use list comprehension with range and slicing
token_batches = [tokens[i:i+4] for i in range(0, len(tokens), 4)]

# 4. Calculate moving average of scores with window size 3
#    Format: List of floats: [avg of first 3, avg of scores 1-3, avg of scores 2-4, ...]
#    Expected: [0.9167, 0.8933, 0.8900, 0.8733, 0.9000, 0.8967, 0.9100, 0.9067, 0.8867, 0.8933]
#    Hint: Use list comprehension with slicing and sum()
group = [sum(scores[i:i+3]) / 3 for i in range(len(scores)-2)]

# 5. Find all positions where a token appears (handling duplicates)
#    For token "the" (case-sensitive), find all indices
#    Format: List of indices: [0, 6] (if "the" appears at those positions)
#    Expected: [6] (only one "the" in lowercase)
#    Hint: Use list comprehension with enumerate
positions_of_the = [i for i, token in enumerate(tokens) if token == "the"]

# 6. Create a list of tuples: (token, score, position) for tokens with score > 0.90
#    Format: [("The", 0.95, 0), ("brown", 0.92, 2), ...]
#    Hint: Use list comprehension with enumerate and zip
#high_score_tokens = [(token, scores[i], i)for i, token in enumerate(tokens) if scores[i] > 0.9]
high_score_tokens = [(token, score, i) for i, (token, score) in enumerate(zip(tokens, scores)) if score > 0.9]

# 7. Split tokens into two lists: first half and second half
#    If odd length, first half should be longer
#    Format: (first_half, second_half)
#    Expected: (["The", "quick", "brown", "fox", "jumps", "over"], ["the", "lazy", "dog", "and", "runs", "fast"])
#    Hint: Use integer division and slicing
split_point = (len(tokens) + 1) // 2
first_half, second_half = tokens[:split_point], tokens[split_point:]  # Your solution here

# 8. BONUS: Create overlapping chunks of size 3 with step size 2
#    Format: [["The", "quick", "brown"], ["brown", "fox", "jumps"], ["jumps", "over", "the"], ...]
#    Hint: Use range with step parameter in list comprehension
overlapping_chunks = [tokens[i:i+3] for i in range(0, len(tokens)-2, 2)]

print(f"Bigrams (first 3): {bigrams[:3] if bigrams else None}")
print(f"Trigrams (first 3): {trigrams[:3] if trigrams else None}")
print(f"Token batches: {token_batches}")
#print(f"Moving average (first 5): {moving_avg[:5] if moving_avg else None}")
print(f"Positions of 'the': {positions_of_the}")
print(f"High score tokens: {high_score_tokens}")
print(f"First half: {first_half}")
print(f"Second half: {second_half}")
print(f"Overlapping chunks (first 3): {overlapping_chunks[:3] if overlapping_chunks else None}")

print("\n" + "=" * 60)
print("ADVANCED EXERCISES COMPLETE!")
print("=" * 60)