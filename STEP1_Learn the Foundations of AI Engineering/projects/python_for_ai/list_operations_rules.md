# Essential Rules for Python List Operations

A comprehensive guide based on common pitfalls and solutions when working with Python lists in AI engineering.

---

## 📋 Table of Contents

1. [Finding All Positions](#1-finding-all-positions-use-enumerate-not-index)
2. [Grouping with Duplicates](#2-grouping-with-duplicates-collect-lists-not-single-values)
3. [Moving Windows](#3-moving-windows-adjust-range-to-prevent-out-of-bounds)
4. [Chunking/Batching](#4-chunkingbatching-use-step-parameter-in-range)
5. [Averaging in Comprehensions](#5-averaging-in-comprehensions-compute-list-once-then-average)
6. [Filtering with "All" Conditions](#6-filtering-with-all-conditions-use-all-function)
7. [Splitting Lists](#7-splitting-lists-use-len--1--2-for-odd-length-handling)
8. [Combining Multiple Lists](#8-combining-multiple-lists-use-zip-instead-of-index-access)
9. [Overlapping Windows](#9-overlapping-windows-calculate-valid-starting-indices)
10. [Sorting with Custom Keys](#10-sorting-with-custom-keys-use-key-parameter-not-manual-extraction)
11. [Slicing Patterns](#11-slicing-patterns-remember-negative-indices-and-steps)
12. [List Comprehension Order](#12-list-comprehensions-order-matters)

---

## 1. Finding All Positions: Use `enumerate()`, Not `.index()`

### Problem
`tokens.index("the")` always returns the **first occurrence**, even if the value appears multiple times.

### Rule
Use `enumerate()` to get the **actual position** of each element.

### Example

```python
# ❌ WRONG: Only finds first occurrence
positions = [tokens.index(token) for token in tokens if token == "the"]
# If "the" appears at indices 2, 5, 8, this returns [2, 2, 2]

# ✅ CORRECT: Finds all positions
positions = [i for i, token in enumerate(tokens) if token == "the"]
# Returns [2, 5, 8] - actual positions
```

### When to Use
- Finding all occurrences of a value
- Need actual index positions (not just first match)
- Working with duplicate values

---

## 2. Grouping with Duplicates: Collect Lists, Not Single Values

### Problem
Dictionary comprehensions **overwrite values** when keys repeat, keeping only the last value.

### Rule
When grouping items that share the same key, **collect them into lists**.

### Example

```python
# ❌ WRONG: Only keeps last value for each key
grouped = {item["key"]: item for item in items}
# If multiple items have key="A", only the last one is kept

# ✅ CORRECT: Collects all values into lists
unique_keys = set(item["key"] for item in items)
grouped = {
    key: [item for item in items if item["key"] == key]
    for key in unique_keys
}
# All items with key="A" are collected in a list
```

### When to Use
- Grouping data by a common attribute
- Multiple items share the same key
- Need to preserve all values, not just one

---

## 3. Moving Windows: Adjust Range to Prevent Out-of-Bounds

### Problem
Using `range(len(list))` for sliding windows can access indices **beyond the list**, creating incomplete windows.

### Rule
For window size `w`, use `range(len(list) - w + 1)` to ensure all windows are complete.

### Example

```python
scores = [0.95, 0.88, 0.92, 0.85, 0.90]

# ❌ WRONG: Last windows are incomplete
windows = [scores[i:i+3] for i in range(len(scores))]
# When i=4: scores[4:7] = [0.90] (only 1 element, not 3!)

# ✅ CORRECT: All windows have exactly 3 elements
windows = [scores[i:i+3] for i in range(len(scores) - 2)]
# range(3) = [0, 1, 2]
# i=0: scores[0:3] = [0.95, 0.88, 0.92] ✓
# i=1: scores[1:4] = [0.88, 0.92, 0.85] ✓
# i=2: scores[2:5] = [0.92, 0.85, 0.90] ✓
```

### Formula
- Window size = `w`
- Valid starting indices: `0` to `len(list) - w`
- Use: `range(len(list) - w + 1)`

### When to Use
- Moving averages
- N-grams (bigrams, trigrams)
- Sliding window analysis
- Any operation requiring fixed-size windows

---

## 4. Chunking/Batching: Use Step Parameter in `range()`

### Problem
Using `range(len(list) - batch_size)` steps by 1, creating **overlapping chunks** instead of separate batches.

### Rule
Use `range(start, stop, step)` where **step equals the batch size**.

### Example

```python
tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy"]

# ❌ WRONG: Creates overlapping chunks
batches = [tokens[i:i+4] for i in range(len(tokens) - 4)]
# range(4) = [0, 1, 2, 3] - overlapping!

# ✅ CORRECT: Non-overlapping batches
batches = [tokens[i:i+4] for i in range(0, len(tokens), 4)]
# range(0, 8, 4) = [0, 4] - separate batches!
# Result: [["The", "quick", "brown", "fox"], ["jumps", "over", "the", "lazy"]]
```

### Pattern
```python
# For batch size b:
batches = [list[i:i+b] for i in range(0, len(list), b)]
```

### When to Use
- Creating non-overlapping batches
- Processing data in chunks
- Batch processing for ML models

---

## 5. Averaging in Comprehensions: Compute List Once, Then Average

### Problem
Creating the list **twice** in the comprehension (once for `sum()`, once for `len()`) is inefficient.

### Rule
Use nested comprehension or two-step approach to **compute once, then average**.

### Example

```python
# ❌ INEFFICIENT: Computes list twice
avg = {
    key: sum([x for x in items if x.key == key]) / 
         len([x for x in items if x.key == key])
    for key in keys
}

# ✅ EFFICIENT: Compute once, then average
grouped = {
    key: [x for x in items if x.key == key] 
    for key in keys
}
avg = {
    key: sum(values) / len(values) 
    for key, values in grouped.items()
}

# ✅ ALTERNATIVE: One-liner with nested comprehension
avg = {
    model: sum(acc_list) / len(acc_list)
    for model in unique_models
    for acc_list in [[result["accuracy"] for result in results if result["model"] == model]]
}
```

### When to Use
- Calculating averages per group
- Any aggregation requiring both sum and count
- Performance optimization in comprehensions

---

## 6. Filtering with "All" Conditions: Use `all()` Function

### Problem
Checking individual items includes models if **ANY result** meets criteria, not all.

### Rule
Use `all()` to verify **every item** in a group meets the condition.

### Example

```python
# ❌ WRONG: Includes if ANY result meets criteria
models = list(set([m["model"] for m in results if m["score"] > 0.9]))
# If Model A has scores [0.95, 0.85], it's included (0.95 > 0.9)

# ✅ CORRECT: Only includes if ALL results meet criteria
unique_models = set(m["model"] for m in results)
models = [
    model for model in unique_models
    if all(r["score"] > 0.9 for r in results if r["model"] == model)
]
# Model A is NOT included (0.85 < 0.9)
```

### When to Use
- Filtering groups where all items must meet criteria
- Quality control checks
- Validating all results for a category

---

## 7. Splitting Lists: Use `(len + 1) // 2` for Odd-Length Handling

### Problem
`len // 2` makes **second half longer** when length is odd (should be first half).

### Rule
Use `(len + 1) // 2` to make **first half longer** when length is odd.

### Example

```python
tokens = ["a", "b", "c", "d", "e"]  # 5 elements (odd)

# ❌ WRONG: Second half longer for odd lengths
split = len(tokens) // 2  # 2
first = tokens[:2]   # ["a", "b"] (2 elements)
second = tokens[2:]   # ["c", "d", "e"] (3 elements) ✗

# ✅ CORRECT: First half longer for odd lengths
split = (len(tokens) + 1) // 2  # 3
first = tokens[:3]   # ["a", "b", "c"] (3 elements) ✓
second = tokens[3:]  # ["d", "e"] (2 elements) ✓
```

### Formula
```python
split_point = (len(list) + 1) // 2
first_half, second_half = list[:split_point], list[split_point:]
```

### Why It Works
- Even length: `(12 + 1) // 2 = 6` (equal halves)
- Odd length: `(11 + 1) // 2 = 6` (first half gets extra element)

### When to Use
- Splitting data into halves
- Train/test splits
- Dividing lists with preference for first half

---

## 8. Combining Multiple Lists: Use `zip()` Instead of Index Access

### Problem
Accessing `list2[i]` requires **keeping track of indices** manually, error-prone.

### Rule
Use `zip()` to **pair elements** from multiple lists naturally.

### Example

```python
tokens = ["The", "quick", "brown"]
scores = [0.95, 0.88, 0.92]

# ❌ LESS CLEAR: Manual index management
pairs = [(tokens[i], scores[i]) for i in range(len(tokens))]

# ✅ CLEAR: zip() pairs elements automatically
pairs = [(token, score) for token, score in zip(tokens, scores)]

# With enumerate for indices:
pairs = [
    (token, score, i) 
    for i, (token, score) in enumerate(zip(tokens, scores))
]
```

### When to Use
- Combining parallel lists
- Processing related data together
- Avoiding manual index management

---

## 9. Overlapping Windows: Calculate Valid Starting Indices

### Problem
Using confusing index shifts (`i-1`) makes code **hard to understand** and debug.

### Rule
Calculate **valid starting indices directly**, then slice.

### Example

```python
# ❌ CONFUSING: Index shifting
chunks = [tokens[i-1:i+2] for i in range(1, len(tokens), 2)]
# Hard to understand: why i-1? why start at 1?

# ✅ CLEAR: Direct calculation
# Overlapping chunks of size 3, step size 2
chunks = [tokens[i:i+3] for i in range(0, len(tokens)-2, 2)]
# Start at 0, step by 2, stop before out-of-bounds
```

### Pattern
```python
# For chunk size c, step size s:
chunks = [list[i:i+c] for i in range(0, len(list)-c+1, s)]
```

### When to Use
- Overlapping n-grams
- Sliding windows with step > 1
- Any overlapping chunking pattern

---

## 10. Sorting with Custom Keys: Use `key` Parameter, Not Manual Extraction

### Problem
Manually extracting values for sorting is **verbose** and error-prone.

### Rule
Use `sorted()` with `key=lambda` to specify **what to sort by**.

### Example

```python
items = [("GPT-4", 0.92), ("Claude", 0.89), ("GPT-3", 0.85)]

# ❌ VERBOSE: Manual extraction
sorted_items = sorted([(item[1], item[0]) for item in items])

# ✅ CLEAN: Use key parameter
sorted_items = sorted(items, key=lambda x: x[1])  # Sort by score
sorted_items = sorted(items, key=lambda x: x[1], reverse=True)  # Descending
```

### Advanced Example
```python
# Sort models by their scores
models = ["GPT-4", "Claude", "GPT-3"]
scores = [0.92, 0.89, 0.85]

# Sort models by corresponding scores
sorted_models = [
    model for model, score in 
    sorted(zip(models, scores), key=lambda x: x[1])
]
```

### When to Use
- Sorting by a specific field
- Complex sorting criteria
- Sorting tuples or dictionaries

---

## 11. Slicing Patterns: Remember Negative Indices and Steps

### Rule
Master these slicing patterns for efficient list operations.

### Common Patterns

```python
tokens = ["a", "b", "c", "d", "e", "f"]

# Basic slicing
tokens[:3]      # ["a", "b", "c"] - first 3
tokens[3:]      # ["d", "e", "f"] - from index 3 to end
tokens[2:5]     # ["c", "d", "e"] - indices 2 to 4

# Negative indices
tokens[-3:]     # ["d", "e", "f"] - last 3
tokens[:-2]     # ["a", "b", "c", "d"] - all except last 2

# Steps
tokens[::2]     # ["a", "c", "e"] - every 2nd element
tokens[1::2]    # ["b", "d", "f"] - every 2nd starting from 1
tokens[::-1]    # ["f", "e", "d", "c", "b", "a"] - reversed

# Combined
tokens[1:5:2]   # ["b", "d"] - from 1 to 4, step 2
```

### When to Use
- Extracting sublists
- Reversing lists
- Skipping elements
- Getting first/last N elements

---

## 12. List Comprehensions: Order Matters

### Rule
Put filters (`if`) **after the loop**, transformations before.

### Example

```python
# ✅ CORRECT ORDER
result = [transform(x) for x in items if condition(x)]
# Transform first, then filter (more efficient)

# Example:
scores = [0.45, 0.92, 0.67, 0.33, 0.88]
high_squared = [score**2 for score in scores if score >= 0.5]
# [0.8464, 0.4489, 0.7744]
```

### When to Use
- Filtering and transforming data
- Conditional transformations
- Data preprocessing

---

## 🎯 Quick Reference Checklist

When working with lists, ask yourself:

- [ ] **Do I need actual positions?** → Use `enumerate()`, not `.index()`
- [ ] **Am I grouping items?** → Collect into lists, not single values
- [ ] **Am I creating windows?** → Adjust range to prevent out-of-bounds
- [ ] **Am I chunking?** → Use step parameter in `range()`
- [ ] **Do I need "all" to match?** → Use `all()` function
- [ ] **Am I combining lists?** → Use `zip()` instead of manual indexing
- [ ] **Is the length odd?** → Use `(len + 1) // 2` for splitting
- [ ] **Am I averaging?** → Compute list once, then average
- [ ] **Am I sorting?** → Use `key` parameter
- [ ] **Do I need overlapping chunks?** → Calculate valid indices directly

---

## 📚 Common Patterns Cheat Sheet

### Window Operations
```python
# Window size w, list length n
windows = [list[i:i+w] for i in range(n - w + 1)]
```

### Chunking
```python
# Batch size b
batches = [list[i:i+b] for i in range(0, len(list), b)]
```

### Overlapping Chunks
```python
# Chunk size c, step size s
chunks = [list[i:i+c] for i in range(0, len(list)-c+1, s)]
```

### Grouping
```python
# Group items by key
grouped = {
    key: [item for item in items if item["key"] == key]
    for key in unique_keys
}
```

### Filtering All
```python
# Only include if ALL items meet condition
result = [
    group for group in groups
    if all(condition(item) for item in group)
]
```

### Splitting
```python
# Split in half (first half longer if odd)
split = (len(list) + 1) // 2
first, second = list[:split], list[split:]
```

---

## 💡 Pro Tips

1. **Always test edge cases**: Empty lists, single elements, odd/even lengths
2. **Use descriptive variable names**: `split_point` instead of `s`, `window_size` instead of `w`
3. **Break complex comprehensions**: Sometimes two lines are clearer than one
4. **Verify ranges**: Check that your range doesn't go out of bounds
5. **Use `zip()` liberally**: It's more Pythonic than manual indexing

---

*Last updated: Based on exercises from `lists_exercises.py`*

