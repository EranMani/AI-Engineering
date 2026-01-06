# 1. Tokenized text processing
tokens = ["The", "quick", "brown", "fox"]
tokens.append("jumps")                    # Add token
tokens.extend(["over", "the", "lazy"])   # Add multiple
tokens.insert(0, "Once")                  # Insert at beginning

# 2. Conversation history management
conversation = []
conversation.append({"role": "user", "content": "Hello"})
conversation.append({"role": "assistant", "content": "Hi there!"})

# 3. Batch processing
scores = [0.85, 0.92, 0.78, 0.95]
avg = sum(scores) / len(scores)           # Calculate average
top_score = max(scores)                   # Find maximum

# 4. List comprehensions for data transformation
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]          # [1, 4, 9, 16, 25]
evens = [x for x in numbers if x % 2 == 0] # [2, 4]

# 5. Enumerate for indexed iteration (very common!)
for i, token in enumerate(tokens):
    print(f"Token {i}: {token}")

# 6. Zip for parallel iteration
features = [0.1, 0.2, 0.3, 0.4]
labels = ["A", "B", "C", "D"]
for feature, label in zip(features, labels):
    print(f"{label}: {feature}")

# 7. Filtering and mapping
numbers = [1, 2, 3, 4, 5, 6]
evens = list[int](filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6]
doubled = list(map(lambda x: x * 2, numbers))       # [2, 4, 6, 8, 10, 12]

# 8. Slicing for sublists
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
first_three = data[:3]                    # [0, 1, 2]
last_three = data[-3:]                     # [7, 8, 9]
middle = data[3:7]                         # [3, 4, 5, 6]
reversed_copy = data[::-1]                 # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 9. Checking membership and counting
if "brown" in tokens:
    count = tokens.count("brown")
    
# 10. Sorting (in-place vs new list)
scores = [0.85, 0.92, 0.78, 0.95]
scores.sort()                              # Modifies original
sorted_scores = sorted(scores, reverse=True)  # Returns new list