# ============================================================================
# EXERCISE 1: Basic Dictionary Operations
# ============================================================================
from email.policy import default
from typing import Any, DefaultDict

from python_for_ai.lists_exercises import groupded_by_test_id


print("\n" + "=" * 60)
print("EXERCISE 1: Basic Dictionary Operations")
print("=" * 60)

# Scenario: Managing AI model configurations
model_config = {
    "model_name": "GPT-4",
    "temperature": 0.7,
    "max_tokens": 2048
}

# TODO: Complete the following operations:

# 1. Access the "temperature" value
temperature = model_config.get("temperature", 0.5)

# 2. Safely get "top_p" value with default 0.9 (use .get())
top_p = model_config.get("top_p", 0.9)

# 3. Check if "system_prompt" key exists (use 'in' operator)
has_system_prompt = "system_prompt" in model_config

# 4. Add a new key "frequency_penalty" with value 0.0
#    Use: model_config[...] = ...
model_config["frequency_penalty"] = 0.0

# 5. Update the dictionary with these new settings:
#    {"top_p": 0.9, "presence_penalty": 0.0}
#    Use: model_config.update(...)
model_config.update({"top_p": 0.9, "presence_penalty": 0.0})

# 6. Get all keys as a list
config_keys = list(model_config.keys())

# 7. Get all values as a list
config_values = list(model_config.values())

# Expected outputs:
# temperature: 0.7
# top_p: 0.9 (default)
# has_system_prompt: False
# config_keys: ['model_name', 'temperature', 'max_tokens', 'frequency_penalty', 'top_p', 'presence_penalty']
# config_values: ['GPT-4', 0.7, 2048, 0.0, 0.9, 0.0]

print(f"Temperature: {temperature}")
print(f"Top P: {top_p}")
print(f"Has system prompt: {has_system_prompt}")
print(f"Keys: {config_keys}")
print(f"Values: {config_values}")



# ============================================================================
# EXERCISE 2: Iterating Over Dictionaries
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 2: Iterating Over Dictionaries")
print("=" * 60)

# Scenario: Processing word embeddings
word_embeddings = {
    "python": [0.2, 0.5, 0.1, 0.8],
    "ai": [0.9, 0.3, 0.7, 0.2],
    "machine_learning": [0.6, 0.4, 0.9, 0.5]
}

# TODO: Complete the following:

# 1. Print each word and its embedding vector
#    Format: "python: [0.2, 0.5, 0.1, 0.8]"
print("Word Embeddings:")
for k,v in word_embeddings.items():
    print(f"{k}: {v}")
# Write your loop here using .items()

# 2. Create a list of words (keys only)
words_list = list(word_embeddings.keys())

# 3. Create a list of all embedding vectors (values only)
embeddings_list = list(word_embeddings.values())

# 4. Find words with embedding vectors longer than 3 elements
#    Format: List of words
long_embedding_words = [word for word, vectors in word_embeddings.items() if len(vectors) > 3]

print(f"\nWords list: {words_list}")
print(f"Embeddings list: {embeddings_list}")
print(f"Words with long embeddings: {long_embedding_words}")


# ============================================================================
# EXERCISE 3: Dictionary Comprehensions
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 3: Dictionary Comprehensions")
print("=" * 60)

# Scenario: Processing model performance scores
model_scores = {
    "GPT-4": 0.92,
    "Claude": 0.89,
    "GPT-3": 0.85,
    "BERT": 0.78,
    "T5": 0.88
}

# TODO: Use dictionary comprehensions to:

# 1. Create a new dict with scores multiplied by 100 (convert to percentages)
#    Format: {"GPT-4": 92, "Claude": 89, ...}
percentages = {model:int(score * 100) for model, score in model_scores.items()}

# 2. Filter models with score >= 0.85
#    Format: {"GPT-4": 0.92, "Claude": 0.89, ...}
high_performers = {model:score for model,score in model_scores.items() if score >= 0.85}

# 3. Create a dict with model names in uppercase as keys
#    Format: {"GPT-4": 0.92, "CLAUDE": 0.89, ...}
uppercase_keys = {model.upper():score for model,score in model_scores.items()}

# 4. Create a dict mapping scores to model names (invert the dictionary)
#    Format: {0.92: "GPT-4", 0.89: "Claude", ...}
#    Note: This only works if scores are unique!
score_to_model = {score:model for model,score in model_scores.items()}

print(f"Percentages: {percentages}")
print(f"High performers: {high_performers}")
print(f"Uppercase keys: {uppercase_keys}")
print(f"Score to model: {score_to_model}")



# ============================================================================
# EXERCISE 4: Understanding .setdefault() - Building Lists in Dicts
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 4: Understanding .setdefault() - Building Lists in Dicts")
print("=" * 60)

# Scenario: Grouping conversation messages by role
# .setdefault() is PERFECT when you need to initialize a list/dict if it doesn't exist,
# then immediately use it. It's a common pattern for grouping data.

messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "I'm doing well!"},
    {"role": "system", "content": "You are helpful"}
]

# TODO: Group messages by role using .setdefault()
# The pattern is: dict.setdefault(key, []).append(value)
# This means: "If key doesn't exist, create it with value [], then append"

grouped_by_role = {}

# Method 1: Using .setdefault() (RECOMMENDED for this pattern)
for message in messages:
    role = message["role"]
    content = message["content"]
    # TODO: Use .setdefault() to create list if needed, then append content
    # Format: grouped_by_role.setdefault(role, []).append(content)
    # Your solution here
    grouped_by_role.setdefault(role, []).append(content)

# Expected: {"user": ["Hello", "How are you?"], "assistant": [...], "system": [...]}

print("Grouped by role:")
for role, contents in grouped_by_role.items():
    print(f"  {role}: {contents}")

# TODO: Now try the same without .setdefault() (more verbose)
grouped_by_role_manual = {}
for message in messages:
    role = message["role"]
    content = message["content"]
    # TODO: Manual approach - check if key exists, create if not, then append
    # Your solution here (if-else approach)
    if role not in grouped_by_role_manual:
        grouped_by_role_manual[role] = []

    grouped_by_role_manual[role].append(content)

print("\nManual approach (same result):")
for role, contents in grouped_by_role_manual.items():
    print(f"  {role}: {contents}")

# KEY INSIGHT: .setdefault() saves you from writing if-else checks!



# ============================================================================
# EXERCISE 5: Understanding .setdefault() - Counting with Defaults
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 5: Understanding .setdefault() - Counting")
print("=" * 60)

# Scenario: Counting tokens in text
# .setdefault() is useful when you need a default value (like 0 for counting)

tokens = ["the", "cat", "sat", "on", "the", "mat", "the", "cat", "slept"]

# TODO: Count token occurrences using .setdefault()
token_counts = {}

for token in tokens:
    # TODO: Use .setdefault() to initialize count to 0 if key doesn't exist,
    # then increment by 1
    # Pattern: token_counts.setdefault(token, 0) += 1 won't work!
    # Instead: token_counts[token] = token_counts.setdefault(token, 0) + 1
    # Your solution here
    token_counts[token] = token_counts.setdefault(token, 0) + 1

# Expected: {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "slept": 1}

print("Token counts:")
for token, count in token_counts.items():
    print(f"  {token}: {count}")

# NOTE: For counting, there's a BETTER way (we'll learn in Exercise 7!)

# ============================================================================
# EXERCISE 6: Merging and Updating Dictionaries
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 6: Merging and Updating Dictionaries")
print("=" * 60)

# Scenario: Combining configuration settings
default_config = {
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 0.9
}

user_config = {
    "temperature": 0.8,  # User wants different temperature
    "frequency_penalty": 0.5  # User adds new setting
}

# TODO: Complete the following:

# 1. Merge user_config into default_config using .update()
#    Note: This modifies default_config in place!
merged_config = default_config.copy()  # Make a copy first
# TODO: Update merged_config with user_config
# Your solution here
merged_config.update(user_config)

# 2. Merge using dictionary unpacking (creates new dict, doesn't modify original)
#    Format: {**dict1, **dict2}
merged_config_new = {**merged_config, **user_config}

# 3. Create a config that prioritizes user_config over default_config
#    (user values override defaults)
final_config = {**default_config, **user_config}

print(f"Merged (update): {merged_config}")
print(f"Merged (unpacking): {merged_config_new}")
print(f"Final config: {final_config}")



# ============================================================================
# EXERCISE 7: Introduction to defaultdict - Easier Counting
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 7: Introduction to defaultdict - Easier Counting")
print("=" * 60)

# Scenario: Counting tokens (same as Exercise 5, but easier!)
# defaultdict automatically creates missing keys with a default value
# This eliminates the need for .setdefault() or if-else checks

from collections import defaultdict

tokens = ["the", "cat", "sat", "on", "the", "mat", "the", "cat", "slept"]

# TODO: Count tokens using defaultdict
# Step 1: Create a defaultdict with int as default (defaults to 0)
token_counts = defaultdict(int)

# Step 2: Count tokens (no need for .setdefault() or if checks!)
for token in tokens:
    # TODO: Just increment directly - defaultdict handles missing keys!
    # Your solution here
    token_counts[token] += 1

# Expected: {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "slept": 1}

print("Token counts (using defaultdict):")
for token, count in token_counts.items():
    print(f"  {token}: {count}")

# KEY INSIGHT: defaultdict(int) is PERFECT for counting - no initialization needed!


# ============================================================================
# EXERCISE 8: defaultdict with Lists - Grouping Made Easy
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 8: defaultdict with Lists - Grouping Made Easy")
print("=" * 60)

# Scenario: Grouping messages by role (same as Exercise 4, but easier!)
# defaultdict(list) automatically creates empty lists for missing keys

from collections import defaultdict

messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"},
    {"role": "assistant", "content": "I'm doing well!"},
    {"role": "system", "content": "You are helpful"}
]

# TODO: Group messages using defaultdict(list)
grouped_by_role = defaultdict(list)

for message in messages:
    role = message["role"]
    content = message["content"]
    # TODO: Just append directly - defaultdict creates list if needed!
    # Your solution here
    grouped_by_role[role].append(content)

print("Grouped by role (using defaultdict):")
for role, contents in grouped_by_role.items():
    print(f"  {role}: {contents}")

# KEY INSIGHT: defaultdict(list) eliminates .setdefault() for grouping!


# ============================================================================
# EXERCISE 9: Introduction to Counter - Automatic Counting
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 9: Introduction to Counter - Automatic Counting")
print("=" * 60)

# Scenario: Counting tokens (even easier than defaultdict!)
# Counter is a special dictionary designed specifically for counting
# It automatically counts items from any iterable

from collections import Counter

tokens = ["the", "cat", "sat", "on", "the", "mat", "the", "cat", "slept"]

# TODO: Count tokens using Counter
# It's as simple as: Counter(iterable)
token_counts = Counter(tokens)

# Expected: Counter({"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "slept": 1})

print("Token counts (using Counter):")
print(token_counts)

# TODO: Get the most common tokens
# Use: .most_common(n) to get top N items
top_3_tokens = token_counts.most_common(3)

print(f"\nTop 3 tokens: {top_3_tokens}")

# KEY INSIGHT: Counter is the EASIEST way to count items!


# ============================================================================
# EXERCISE 10: Removing Items from Dictionaries
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 10: Removing Items from Dictionaries")
print("=" * 60)

# Scenario: Managing model configurations
config = {
    "model_name": "GPT-4",
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 0.9,
    "debug": True,
    "verbose": False
}

# TODO: Complete the following:

# 1. Remove "debug" key using del
#    Use: del config["key"]
del config["debug"]

# 2. Remove "verbose" and get its value using .pop()
verbose_value = config.pop("verbose")

# 3. Safely remove "system_prompt" with default "None" if it doesn't exist
system_prompt = config.pop("system_prompt", "None")

# 4. Remove and return the last (key, value) pair using .popitem()
last_item = config.popitem()

# 5. Create a production config without debug/verbose keys
#    Use dictionary comprehension to filter
production_config = {key:param for key,param in config.items() if key not in ["verbose", "debug"]}

print(f"Verbose value: {verbose_value}")
print(f"System prompt: {system_prompt}")
print(f"Last item: {last_item}")
print(f"Production config: {production_config}")

print("\n" + "=" * 60)
print("EXERCISES COMPLETE!")
print("=" * 60)


# ============================================================================
# EXERCISE 11: Advanced Data Processing - Nested Dictionaries and Aggregation
# ============================================================================
print("\n" + "=" * 60)
print("EXERCISE 11: Advanced Data Processing - Nested Dictionaries")
print("=" * 60)

from collections import defaultdict

# Scenario: Processing AI model performance data across multiple test runs
# Each model has been tested on multiple datasets with different metrics

model_results = [
    {"model": "GPT-4", "dataset": "test_set_1", "accuracy": 0.92, "latency_ms": 150, "cost": 0.03},
    {"model": "GPT-4", "dataset": "test_set_2", "accuracy": 0.88, "latency_ms": 145, "cost": 0.03},
    {"model": "Claude", "dataset": "test_set_1", "accuracy": 0.89, "latency_ms": 180, "cost": 0.02},
    {"model": "Claude", "dataset": "test_set_2", "accuracy": 0.91, "latency_ms": 175, "cost": 0.02},
    {"model": "GPT-3", "dataset": "test_set_1", "accuracy": 0.85, "latency_ms": 200, "cost": 0.01},
    {"model": "GPT-3", "dataset": "test_set_2", "accuracy": 0.83, "latency_ms": 195, "cost": 0.01},
    {"model": "BERT", "dataset": "test_set_1", "accuracy": 0.78, "latency_ms": 50, "cost": 0.005},
    {"model": "BERT", "dataset": "test_set_2", "accuracy": 0.80, "latency_ms": 55, "cost": 0.005},
]

# TODO: Complete the following advanced operations:

# 1. Create a nested dictionary structure grouped by model
#    Format: {"GPT-4": [result1, result2], "Claude": [result1, result2], ...}
#    Use defaultdict(list) for cleaner code
grouped_by_model = defaultdict(list)

for result in model_results:
    model = result["model"]
    grouped_by_model[model].append(result)

# 2. Calculate average metrics for each model
#    Format: {"GPT-4": {"avg_accuracy": 0.90, "avg_latency": 147.5, "avg_cost": 0.03}, ...}
#    Hint: Use dictionary comprehension with sum() and len()
model_averages = {model:{"avg_accuracy": sum(r["accuracy"] for r in results) / len(results),
                         "avg_latency": sum(r["latency_ms"] for r in results) / len(results),
                         "avg_cost": sum(r["cost"] for r in results) / len(results)} for model, results in grouped_by_model.items()}

# 3. Find the best performing model for each dataset
#    Format: {"test_set_1": {"model": "GPT-4", "accuracy": 0.92}, "test_set_2": {...}}
#    Hint: Group by dataset first, then find max accuracy
grouped_by_dataset = defaultdict(list)

for result in model_results:
    dataset = result["dataset"]
    grouped_by_dataset[dataset].append({"model": result["model"], "accuracy": result["accuracy"]})

best_per_dataset = {}
for dataset, results in grouped_by_dataset.items():
    best_result = max(results, key=lambda r: r["accuracy"])
    best_per_dataset[dataset] = {
        "model": best_result["model"],
        "accuracy": best_result["accuracy"]
    }

# 4. Create a ranking of models by average accuracy (descending)
#    Format: [("GPT-4", 0.90), ("Claude", 0.90), ("GPT-3", 0.84), ("BERT", 0.79)]
#    Handle ties appropriately
model_rankings = [(model, sum(r["accuracy"] for r in results) / len(results)) for model, results in grouped_by_model.items()]
model_rankings = sorted(model_rankings, key= lambda x: x[1], reverse=True)

# 5. Calculate cost-effectiveness score for each model
#    Formula: avg_accuracy / avg_cost (higher is better)
#    Format: {"GPT-4": 30.0, "Claude": 45.0, ...}

cost_effectiveness = {model: metrics["avg_accuracy"] / metrics["avg_cost"] for model, metrics in model_averages.items()}

# 6. Create a comprehensive summary dictionary
#    Format: {
#        "GPT-4": {
#            "results": [list of results],
#            "avg_accuracy": 0.90,
#            "avg_latency": 147.5,
#            "avg_cost": 0.03,
#            "cost_effectiveness": 30.0,
#            "rank": 1
#        },
#        ...
#    }

# Build comprehensive summary with proper ranking
comprehensive_summary = {}
current_rank = 1
prev_accuracy = None

for i, (model, accuracy) in enumerate(model_rankings, start=1):
    # Update rank if accuracy changed (handles ties)
    if prev_accuracy is not None and accuracy != prev_accuracy:
        current_rank = i
    
    comprehensive_summary[model] = {
        "results": grouped_by_model[model],
        "avg_accuracy": model_averages[model]["avg_accuracy"],
        "avg_latency": model_averages[model]["avg_latency"],
        "avg_cost": model_averages[model]["avg_cost"],
        "cost_effectiveness": cost_effectiveness[model],
        "rank": current_rank
    }
    
    prev_accuracy = accuracy





print(f"Grouped by model: {list(grouped_by_model.keys()) if grouped_by_model else None}")
print(f"\nModel averages: {model_averages}")
print(f"\nBest per dataset: {best_per_dataset}")
print(f"\nModel rankings: {model_rankings}")
print(f"\nCost effectiveness: {cost_effectiveness}")
print(f"\nComprehensive summary keys: {list(comprehensive_summary.keys()) if comprehensive_summary else None}")