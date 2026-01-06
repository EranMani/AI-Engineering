# Essential Rules for Python Dictionary Operations

A comprehensive guide based on common pitfalls and solutions when working with Python dictionaries in AI engineering.

---

## 📋 Table of Contents

1. [Safe Value Access: Use `.get()` Instead of Direct Access](#1-safe-value-access-use-get-instead-of-direct-access)
2. [Grouping Items: Use `defaultdict(list)` Instead of Manual Checks](#2-grouping-items-use-defaultdictlist-instead-of-manual-checks)
3. [Counting Items: Use `Counter` or `defaultdict(int)`](#3-counting-items-use-counter-or-defaultdictint)
4. [When to Use `.setdefault()`](#4-when-to-use-setdefault)
5. [Merging Dictionaries: Order Matters](#5-merging-dictionaries-order-matters)
6. [Dictionary Comprehensions: Transform, Don't Build Iteratively](#6-dictionary-comprehensions-transform-dont-build-iteratively)
7. [Nested Dictionary Access: Safe Navigation](#7-nested-dictionary-access-safe-navigation)
8. [Grouping with Aggregations: Reuse Intermediate Results](#8-grouping-with-aggregations-reuse-intermediate-results)
9. [Finding Best Items: Use `max()` with `key` Parameter](#9-finding-best-items-use-max-with-key-parameter)
10. [Ranking: Calculate from Position, Not Values](#10-ranking-calculate-from-position-not-values)
11. [Inverting Dictionaries: Only Works with Unique Values](#11-inverting-dictionaries-only-works-with-unique-values)
12. [Filtering Dictionaries: Use Comprehensions](#12-filtering-dictionaries-use-comprehensions)
13. [The `popitem()` Method: Remove and Return Items](#13-the-popitem-method-remove-and-return-items)
14. [The `fromkeys()` Trap: Shared Mutable Defaults](#14-the-fromkeys-trap-shared-mutable-defaults)
15. [OrderedDict and LRU Cache: When Order Matters](#15-ordereddict-and-lru-cache-when-order-matters)
16. [Dictionary Views: Efficient Key/Value/Item Iteration](#16-dictionary-views-efficient-keyvalueitem-iteration)

---

## 1. Safe Value Access: Use `.get()` Instead of Direct Access

### Problem
Direct access `dict["key"]` raises `KeyError` if the key doesn't exist, crashing your program.

### Rule
Use `.get(key, default)` for safe access with fallback values.

### Example

```python
config = {"temperature": 0.7, "max_tokens": 2048}

# ❌ WRONG: Raises KeyError if key doesn't exist
top_p = config["top_p"]  # KeyError!

# ✅ CORRECT: Returns None if key doesn't exist
top_p = config.get("top_p")  # Returns None

# ✅ BETTER: Returns default value
top_p = config.get("top_p", 0.9)  # Returns 0.9 if missing
```

### When to Use
- Accessing configuration values
- Working with optional parameters
- API response handling
- Any situation where a key might not exist

---

## 2. Grouping Items: Use `defaultdict(list)` Instead of Manual Checks

### Problem
Manually checking if a key exists before appending is verbose and error-prone.

### Rule
Use `defaultdict(list)` to automatically create empty lists for new keys.

### Example

```python
from collections import defaultdict

messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "How are you?"}
]

# ❌ VERBOSE: Manual checks
grouped = {}
for msg in messages:
    role = msg["role"]
    if role not in grouped:
        grouped[role] = []
    grouped[role].append(msg["content"])

# ✅ CLEAN: defaultdict handles it automatically
grouped = defaultdict(list)
for msg in messages:
    grouped[msg["role"]].append(msg["content"])
# No if-checks needed!
```

### When to Use
- Grouping items by a common attribute
- Building lists of related items
- Any pattern where you append to lists in dictionaries

---

## 3. Counting Items: Use `Counter` or `defaultdict(int)`

### Problem
Manually counting with `.setdefault()` or if-checks is verbose.

### Rule
Use `Counter` for simple counting, or `defaultdict(int)` for more control.

### Example

```python
from collections import Counter, defaultdict

tokens = ["the", "cat", "sat", "on", "the", "mat"]

# ❌ VERBOSE: Manual counting
counts = {}
for token in tokens:
    counts[token] = counts.setdefault(token, 0) + 1

# ✅ SIMPLEST: Counter (best for counting)
counts = Counter(tokens)
# Result: Counter({"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1})

# ✅ ALTERNATIVE: defaultdict(int)
counts = defaultdict(int)
for token in tokens:
    counts[token] += 1  # No initialization needed!
```

### When to Use
- **Counter**: Simple counting from iterables
- **defaultdict(int)**: Counting with additional logic or conditions
- Token counting, frequency analysis, vote counting

---

## 4. When to Use `.setdefault()`

### Problem
`.setdefault()` is useful but often misunderstood. When should you use it?

### Rule
Use `.setdefault()` when you need to **initialize a value if missing, then immediately use it**.

### Example

```python
# ✅ PERFECT USE CASE: Building lists in dictionaries
conversation = {}
conversation.setdefault("messages", []).append("Hello")
# Creates list if missing, then appends

# ✅ PERFECT USE CASE: Counting (though defaultdict is better)
counts = {}
counts[token] = counts.setdefault(token, 0) + 1

# ❌ UNNECESSARY: When defaultdict is better
grouped = {}
for item in items:
    grouped.setdefault(key, []).append(item)
# Better: Use defaultdict(list)

# ❌ WRONG: When you just need a default value
value = my_dict.setdefault("key", "default")
# Better: Use my_dict.get("key", "default")
```

### Key Insight
`.setdefault()` is useful when you need to **initialize AND use** in one step. For most cases, `defaultdict` or `.get()` is cleaner.

### When to Use
- Initializing lists/dicts before appending (if not using defaultdict)
- One-off initialization patterns
- Legacy code compatibility

---

## 5. Merging Dictionaries: Order Matters

### Problem
When merging dictionaries, the order determines which values win when keys overlap.

### Rule
**Later dictionaries override earlier ones** in unpacking: `{**dict1, **dict2}` → dict2 wins.

### Example

```python
default_config = {"temperature": 0.7, "max_tokens": 2048}
user_config = {"temperature": 0.8, "top_p": 0.9}

# ❌ WRONG ORDER: Defaults override user settings
merged = {**user_config, **default_config}
# Result: {"temperature": 0.7, "max_tokens": 2048, "top_p": 0.9}
# User's temperature preference is lost!

# ✅ CORRECT ORDER: User settings override defaults
merged = {**default_config, **user_config}
# Result: {"temperature": 0.8, "max_tokens": 2048, "top_p": 0.9}
# User's preferences are preserved
```

### Pattern
```python
# Priority order: user > defaults
final_config = {**default_config, **user_config}

# Priority order: overrides > user > defaults
final_config = {**default_config, **user_config, **overrides}
```

### When to Use
- Configuration management
- Merging settings from multiple sources
- Creating final configurations with priority

---

## 6. Dictionary Comprehensions: Transform, Don't Build Iteratively

### Problem
Dictionary comprehensions are for **transforming existing data**, not for iteratively building structures.

### Rule
- **Use comprehensions** for transforming/filtering existing dictionaries
- **Use loops** for iteratively building dictionaries (especially with lists)

### Example

```python
# ✅ CORRECT: Transforming existing data
scores = {"GPT-4": 0.92, "Claude": 0.89}
percentages = {model: score * 100 for model, score in scores.items()}
high_scores = {model: score for model, score in scores.items() if score > 0.9}

# ❌ WRONG: Trying to build iteratively
# You CAN'T do this in a comprehension:
grouped = {key: [] for key in keys}  # Creates empty lists
# But you can't append to them in the comprehension!

# ✅ CORRECT: Use loop for building
grouped = defaultdict(list)
for item in items:
    grouped[item["key"]].append(item)
```

### Key Insight
- **Comprehensions**: Transform/filter existing data → `{k: transform(v) for k, v in dict.items()}`
- **Loops**: Build structures iteratively → `for item in items: dict[key].append(item)`

### When to Use
- **Comprehensions**: Filtering, transforming, inverting dictionaries
- **Loops**: Grouping, counting, building nested structures

---

## 7. Nested Dictionary Access: Safe Navigation

### Problem
Accessing nested dictionaries with `dict["key1"]["key2"]` raises `KeyError` if any level is missing.

### Rule
Use `.get()` chains or check each level, or use a helper function.

### Example

```python
nested = {
    "models": {
        "GPT-4": {"score": 0.92, "cost": 0.03}
    }
}

# ❌ WRONG: Raises KeyError if any level missing
score = nested["models"]["GPT-4"]["score"]  # KeyError if "models" missing!

# ✅ CORRECT: Chain .get() calls
score = nested.get("models", {}).get("GPT-4", {}).get("score", 0.0)

# ✅ ALTERNATIVE: Check each level
if "models" in nested and "GPT-4" in nested["models"]:
    score = nested["models"]["GPT-4"].get("score", 0.0)
else:
    score = 0.0
```

### When to Use
- API response handling
- Configuration files with nested structures
- Any deeply nested dictionary access

---

## 8. Grouping with Aggregations: Reuse Intermediate Results

### Problem
Recalculating the same values multiple times is inefficient and hard to read.

### Rule
Calculate aggregations once, then reuse them in subsequent operations.

### Example

```python
# ❌ INEFFICIENT: Recalculating averages multiple times
cost_effectiveness = {
    model: (sum(r["accuracy"] for r in results) / len(results)) / 
           (sum(r["cost"] for r in results) / len(results))
    for model, results in grouped.items()
}

# ✅ EFFICIENT: Calculate once, reuse
model_averages = {
    model: {
        "avg_accuracy": sum(r["accuracy"] for r in results) / len(results),
        "avg_cost": sum(r["cost"] for r in results) / len(results)
    }
    for model, results in grouped.items()
}

cost_effectiveness = {
    model: metrics["avg_accuracy"] / metrics["avg_cost"]
    for model, metrics in model_averages.items()
}
```

### When to Use
- Multiple calculations on the same data
- Building comprehensive summaries
- Performance optimization

---

## 9. Finding Best Items: Use `max()` with `key` Parameter

### Problem
Finding the "best" item requires comparing values, not just getting the max value.

### Rule
Use `max(iterable, key=lambda x: x["field"])` to get the whole item, then extract what you need.

### Example

```python
results = [
    {"model": "GPT-4", "accuracy": 0.92},
    {"model": "Claude", "accuracy": 0.89},
    {"model": "GPT-3", "accuracy": 0.85}
]

# ❌ WRONG: Only gets the accuracy value, not the model
best_accuracy = max(r["accuracy"] for r in results)  # Returns 0.92 only

# ✅ CORRECT: Gets the whole item, then extract fields
best_result = max(results, key=lambda r: r["accuracy"])
best_model = best_result["model"]  # "GPT-4"
best_accuracy = best_result["accuracy"]  # 0.92

# ✅ ONE-LINER: Extract both fields
best = {
    "model": max(results, key=lambda r: r["accuracy"])["model"],
    "accuracy": max(results, key=lambda r: r["accuracy"])["accuracy"]
}
# Note: Calls max() twice - less efficient but readable
```

### When to Use
- Finding best/worst items by a metric
- Ranking and comparisons
- Any "find the item with max/min value" scenario

---

## 10. Ranking: Calculate from Position, Not Values

### Problem
Ranks come from **position in sorted list**, not from the values themselves.

### Rule
Calculate rank from index/position, handling ties by keeping the same rank.

### Example

```python
model_rankings = [("GPT-4", 0.90), ("Claude", 0.90), ("GPT-3", 0.84)]

# ❌ WRONG: Trying to extract rank from tuple values
rank = [r for r in model_rankings if r[0] == model][0][-1]  # Gets accuracy, not rank!

# ✅ CORRECT: Calculate rank from position
rank_mapping = {}
current_rank = 1
prev_accuracy = None

for i, (model, accuracy) in enumerate(model_rankings, start=1):
    if prev_accuracy is not None and accuracy != prev_accuracy:
        current_rank = i  # Update rank when accuracy changes
    rank_mapping[model] = current_rank
    prev_accuracy = accuracy

# Result: {"GPT-4": 1, "Claude": 1, "GPT-3": 3}
```

### When to Use
- Creating rankings from sorted data
- Handling ties in rankings
- Displaying position-based information

---

## 11. Inverting Dictionaries: Only Works with Unique Values

### Problem
Inverting `{key: value}` to `{value: key}` only works if all values are unique.

### Rule
Check for unique values before inverting, or handle duplicates explicitly.

### Example

```python
# ✅ WORKS: All values are unique
model_scores = {"GPT-4": 0.92, "Claude": 0.89, "GPT-3": 0.85}
score_to_model = {score: model for model, score in model_scores.items()}
# Result: {0.92: "GPT-4", 0.89: "Claude", 0.85: "GPT-3"}

# ❌ PROBLEM: Duplicate values overwrite keys
model_scores = {"GPT-4": 0.90, "Claude": 0.90, "GPT-3": 0.85}
score_to_model = {score: model for model, score in model_scores.items()}
# Result: {0.90: "Claude", 0.85: "GPT-3"} - GPT-4 is lost!

# ✅ SOLUTION: Group by value if duplicates possible
from collections import defaultdict
score_to_models = defaultdict(list)
for model, score in model_scores.items():
    score_to_models[score].append(model)
# Result: {0.90: ["GPT-4", "Claude"], 0.85: ["GPT-3"]}
```

### When to Use
- Reversing key-value relationships
- Looking up by value instead of key
- Creating reverse mappings

---

## 12. Filtering Dictionaries: Use Comprehensions

### Problem
Manually filtering dictionaries with loops is verbose.

### Rule
Use dictionary comprehensions with conditions for clean filtering.

### Example

```python
config = {
    "temperature": 0.7,
    "max_tokens": 2048,
    "debug": True,
    "verbose": False
}

# ❌ VERBOSE: Manual filtering
production_config = {}
for key, value in config.items():
    if key not in ["debug", "verbose"]:
        production_config[key] = value

# ✅ CLEAN: Dictionary comprehension
production_config = {
    key: value for key, value in config.items()
    if key not in ["debug", "verbose"]
}

# ✅ FILTER BY VALUE
high_scores = {
    model: score for model, score in scores.items()
    if score >= 0.9
}
```

### When to Use
- Removing unwanted keys
- Filtering by value conditions
- Creating subsets of dictionaries

---

## 13. The `popitem()` Method: Remove and Return Items

### Problem
You need to remove and get an item from a dictionary, but don't know or care which key to remove.

### Rule
Use `.popitem()` to remove and return the **last** (key, value) pair. In Python 3.7+, dictionaries maintain insertion order, so this removes the most recently added item.

### Example

```python
config = {
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 0.9,
    "debug": True
}

# Remove and get the last item (most recently added)
last_key, last_value = config.popitem()
# last_key = "debug", last_value = True
# config now: {"temperature": 0.7, "max_tokens": 2048, "top_p": 0.9}

# ✅ USEFUL: Processing items until empty
while config:
    key, value = config.popitem()
    print(f"Processing {key}: {value}")
# Processes items in reverse insertion order

# ⚠️ WARNING: Raises KeyError if dictionary is empty
empty_dict = {}
item = empty_dict.popitem()  # KeyError!
```

### Key Insight
- `.popitem()` returns a **tuple** `(key, value)`
- Removes from the **end** of the dictionary (last inserted item in Python 3.7+)
- Useful for LIFO (Last In, First Out) patterns
- Use with `while dict:` to process all items

### When to Use
- Removing items in reverse order
- Implementing stack-like behavior
- Processing and removing items one by one
- Clearing dictionaries while processing items

---

## 14. The `fromkeys()` Trap: Shared Mutable Defaults

### Problem
Using `dict.fromkeys()` with a mutable default value (like `[]` or `{}`) creates **shared references** - all keys point to the same object!

### Rule
**Never use mutable defaults** with `fromkeys()`. Use dictionary comprehension or loops instead.

### Example

```python
# ❌ DANGEROUS: All keys share the same list!
keys = ["model1", "model2", "model3"]
results = dict.fromkeys(keys, [])
results["model1"].append("result1")
print(results)
# Result: {"model1": ["result1"], "model2": ["result1"], "model3": ["result1"]}
# All keys point to the SAME list object!

# ✅ SAFE: Use immutable defaults
keys = ["model1", "model2", "model3"]
results = dict.fromkeys(keys, 0)  # Immutable (int) is safe
results["model1"] += 1
print(results)
# Result: {"model1": 1, "model2": 0, "model3": 0} ✓

# ✅ CORRECT: Use dictionary comprehension for mutable defaults
keys = ["model1", "model2", "model3"]
results = {key: [] for key in keys}  # Each key gets its own list
results["model1"].append("result1")
print(results)
# Result: {"model1": ["result1"], "model2": [], "model3": []} ✓

# ✅ ALTERNATIVE: Use defaultdict
from collections import defaultdict
results = defaultdict(list)  # Automatically creates new lists
```

### Key Insight
- `fromkeys()` **shares** the default value object across all keys
- Mutable objects (lists, dicts) are shared → changes affect all keys
- Immutable objects (int, str, tuple) are safe → each key gets a copy
- **Always use comprehension or defaultdict** for mutable defaults

### When to Use
- **fromkeys()**: Only with immutable defaults (int, str, tuple, None)
- **Comprehension**: When you need mutable defaults (list, dict)
- **defaultdict**: When building incrementally with mutable defaults

---

## 15. OrderedDict and LRU Cache: When Order Matters

### Problem
In Python 3.7+, regular dictionaries maintain insertion order, but `OrderedDict` still has use cases, especially for LRU (Least Recently Used) cache implementations.

### Rule
Use `OrderedDict` when you need explicit ordering control, move-to-end operations, or compatibility with older Python versions. For LRU cache, use `functools.lru_cache` or `OrderedDict` with `.move_to_end()`.

### Example

```python
from collections import OrderedDict
from functools import lru_cache

# ✅ OrderedDict: Explicit ordering with move operations
cache = OrderedDict(maxsize=3)

def get_data(key):
    if key in cache:
        # Move to end (most recently used)
        cache.move_to_end(key)
        return cache[key]
    
    # Fetch new data
    data = fetch_from_source(key)
    
    # Add to cache
    cache[key] = data
    
    # Remove oldest if cache full
    if len(cache) > cache.maxsize:
        cache.popitem(last=False)  # Remove oldest (FIFO)
    
    return data

# ✅ Better: Use functools.lru_cache (Python 3.2+)
@lru_cache(maxsize=128)
def expensive_function(n):
    # Function results are cached automatically
    return n * n * n

# ✅ OrderedDict: Maintaining insertion order (Python < 3.7 compatibility)
# In Python 3.7+, regular dict maintains order, but OrderedDict still useful for:
ordered_config = OrderedDict([
    ("step1", "initialize"),
    ("step2", "process"),
    ("step3", "finalize")
])

# Move items around
ordered_config.move_to_end("step1")  # Move to end
ordered_config.move_to_end("step2", last=False)  # Move to beginning
```

### Key Insight
- **Python 3.7+**: Regular `dict` maintains insertion order
- **OrderedDict**: Still useful for `.move_to_end()` and explicit ordering operations
- **LRU Cache**: Use `@lru_cache` decorator for function memoization
- **Manual LRU**: Use `OrderedDict` with `.move_to_end()` and `.popitem(last=False)`

### When to Use
- **LRU Cache implementation**: Use `OrderedDict` with move operations or `@lru_cache`
- **Explicit ordering control**: Moving items to front/back
- **Python < 3.7 compatibility**: Maintaining insertion order
- **Cache eviction policies**: FIFO, LIFO, LRU patterns

---

## 16. Dictionary Views: Efficient Key/Value/Item Iteration

### Problem
Calling `.keys()`, `.values()`, or `.items()` multiple times creates overhead, and converting to lists uses extra memory.

### Rule
Dictionary views (`.keys()`, `.values()`, `.items()`) are **live, efficient references** to the dictionary's contents. Use them directly for iteration, or convert to lists only when needed.

### Example

```python
config = {
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 0.9
}

# ✅ EFFICIENT: Views are live references (no copying)
keys_view = config.keys()
values_view = config.values()
items_view = config.items()

# Views reflect changes to the dictionary
config["debug"] = True
print(list(keys_view))  # Includes "debug" - view is live!

# ✅ DIRECT ITERATION: Most efficient
for key in config.keys():  # No list conversion needed
    print(key)

for value in config.values():
    print(value)

for key, value in config.items():
    print(f"{key}: {value}")

# ✅ SET OPERATIONS: Views support set-like operations
config1 = {"a": 1, "b": 2, "c": 3}
config2 = {"b": 2, "c": 3, "d": 4}

# Find common keys
common = config1.keys() & config2.keys()  # {"b", "c"}

# Find keys in config1 but not in config2
unique = config1.keys() - config2.keys()  # {"a"}

# ❌ UNNECESSARY: Converting to list when view works
keys_list = list(config.keys())  # Only do this if you need a list!
# Views are already iterable and support set operations
```

### Key Properties

1. **Live Updates**: Views reflect changes to the dictionary immediately
2. **Memory Efficient**: No copying - just references to dictionary contents
3. **Set Operations**: Views support `&`, `|`, `-`, `^` (intersection, union, difference, symmetric difference)
4. **Iterable**: Can be used directly in `for` loops, `in` checks

### When to Use
- **Direct iteration**: Use views directly in loops (most efficient)
- **Set operations**: Comparing keys/values between dictionaries
- **Memory efficiency**: Avoid converting to lists when views work
- **Live updates**: When you need to see dictionary changes immediately

### Common Patterns

```python
# Check if all keys from one dict exist in another
required_keys = {"temperature", "max_tokens"}
if required_keys <= config.keys():  # Subset check
    print("All required keys present")

# Find overlapping keys
overlap = config1.keys() & config2.keys()

# Iterate efficiently
for key, value in config.items():  # Direct iteration
    process(key, value)
```

---

## 🎯 Quick Reference Checklist

When working with dictionaries, ask yourself:

- [ ] **Do I need safe access?** → Use `.get(key, default)`
- [ ] **Am I grouping items?** → Use `defaultdict(list)`
- [ ] **Am I counting items?** → Use `Counter` or `defaultdict(int)`
- [ ] **Am I merging dicts?** → Check order: `{**defaults, **overrides}`
- [ ] **Am I transforming data?** → Use dictionary comprehension
- [ ] **Am I building iteratively?** → Use loop with `defaultdict`
- [ ] **Do I need nested access?** → Chain `.get()` calls
- [ ] **Am I finding best items?** → Use `max()` with `key` parameter
- [ ] **Am I calculating ranks?** → Use position, not values
- [ ] **Are values unique?** → Check before inverting
- [ ] **Do I need mutable defaults?** → Avoid `fromkeys()`, use comprehension
- [ ] **Am I removing items?** → Use `.popitem()` for LIFO patterns
- [ ] **Do I need ordering control?** → Use `OrderedDict` or `@lru_cache`
- [ ] **Am I iterating keys/values?** → Use views directly, don't convert to list

---

## 📚 Common Patterns Cheat Sheet

### Grouping Items
```python
from collections import defaultdict

# Group by key
grouped = defaultdict(list)
for item in items:
    grouped[item["key"]].append(item)
```

### Counting Items
```python
from collections import Counter, defaultdict

# Simple counting
counts = Counter(items)

# Counting with conditions
counts = defaultdict(int)
for item in items:
    if condition(item):
        counts[item["key"]] += 1
```

### Merging Dictionaries
```python
# User overrides defaults
final = {**defaults, **user_config}

# Multiple priority levels
final = {**defaults, **user_config, **overrides}
```

### Safe Nested Access
```python
# Chain .get() calls
value = dict.get("level1", {}).get("level2", {}).get("level3", default)
```

### Finding Best Item
```python
# Get whole item, then extract
best = max(items, key=lambda x: x["score"])
best_model = best["model"]
best_score = best["score"]
```

### Filtering
```python
# Filter by key
filtered = {k: v for k, v in dict.items() if k not in exclude_keys}

# Filter by value
filtered = {k: v for k, v in dict.items() if v >= threshold}
```

### Aggregations
```python
# Calculate averages
averages = {
    key: sum(values) / len(values)
    for key, values in grouped.items()
}

# Reuse for multiple calculations
averages = {...}
ratios = {k: avg1 / avg2 for k, (avg1, avg2) in averages.items()}
```

### Ranking
```python
# Sort first
sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)

# Calculate ranks (handle ties)
ranks = {}
current_rank = 1
prev_score = None
for i, item in enumerate(sorted_items, start=1):
    if prev_score is not None and item["score"] != prev_score:
        current_rank = i
    ranks[item["id"]] = current_rank
    prev_score = item["score"]
```

### popitem() - Remove Last Item
```python
# Remove and return last (key, value) pair
key, value = dict.popitem()

# Process all items until empty (LIFO order)
while config:
    key, value = config.popitem()
    process(key, value)
```

### fromkeys() - Safe Usage
```python
# ✅ SAFE: Immutable defaults
keys = ["a", "b", "c"]
dict_with_zeros = dict.fromkeys(keys, 0)

# ❌ DANGEROUS: Mutable defaults (all keys share same object!)
dict_with_lists = dict.fromkeys(keys, [])  # DON'T DO THIS!

# ✅ CORRECT: Use comprehension for mutable defaults
dict_with_lists = {key: [] for key in keys}
```

### OrderedDict and LRU Cache
```python
from collections import OrderedDict
from functools import lru_cache

# Manual LRU cache with OrderedDict
cache = OrderedDict(maxsize=3)
if key in cache:
    cache.move_to_end(key)  # Mark as recently used
else:
    cache[key] = value
    if len(cache) > cache.maxsize:
        cache.popitem(last=False)  # Remove oldest

# Built-in LRU cache decorator (preferred)
@lru_cache(maxsize=128)
def expensive_function(n):
    return n * n * n
```

### Dictionary Views
```python
# Use views directly (no list conversion needed)
for key in dict.keys():  # Efficient iteration
    process(key)

# Set operations on views
common_keys = dict1.keys() & dict2.keys()
unique_keys = dict1.keys() - dict2.keys()

# Check subset
required = {"key1", "key2"}
if required <= config.keys():
    print("All keys present")
```

---

## 💡 Pro Tips

1. **Prefer `defaultdict` over `.setdefault()`**: Cleaner and more Pythonic
2. **Use `Counter` for simple counting**: It's designed specifically for this
3. **Reuse intermediate results**: Don't recalculate the same aggregations
4. **Chain `.get()` for nested access**: Prevents KeyError crashes
5. **Order matters in merging**: Later dicts override earlier ones
6. **Use comprehensions for transforms**: Loops for building structures
7. **Calculate ranks from position**: Not from tuple values
8. **Check uniqueness before inverting**: Or handle duplicates explicitly
9. **Never use mutable defaults with `fromkeys()`**: Use comprehensions instead
10. **Use `.popitem()` for LIFO patterns**: Removes last inserted item
11. **Use `@lru_cache` for function memoization**: Simpler than manual OrderedDict
12. **Iterate views directly**: Don't convert to lists unless necessary

---

## 🔄 Dictionary vs List Patterns

| Task | List Pattern | Dictionary Pattern |
|------|-------------|-------------------|
| Grouping | `defaultdict(list)` + loop | `defaultdict(list)` + loop |
| Counting | `Counter(items)` | `Counter(items)` or `defaultdict(int)` |
| Filtering | `[x for x in items if condition]` | `{k: v for k, v in dict.items() if condition}` |
| Transforming | `[transform(x) for x in items]` | `{k: transform(v) for k, v in dict.items()}` |
| Finding best | `max(items, key=lambda x: x.field)` | `max(dict.items(), key=lambda x: x[1])` |
| Safe access | `items[i] if i < len(items) else default` | `dict.get(key, default)` |

---

*Last updated: Based on exercises from `dictionary_exercises.py`*

