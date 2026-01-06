my_dict = {"card": "white", 3: "Three"}

my_dict[3]
my_dict.get("card")
my_dict.get("hi", "error")

"card" in my_dict
3 not in my_dict

my_dict["weather"] = "summer"

another_dict = {"numbers": [1,2,3], "phone": 4}
my_dict.update(another_dict)


default = "are you sure?"
my_dict.setdefault("human", default)

del my_dict["human"]

value = my_dict.pop("weather")

value = my_dict.pop("array", "card")

my_dict.popitem()

#my_dict.clear()

my_dict.keys()
my_dict.values()
my_dict.items()

for key, value in my_dict.items():
    print(key, value)

len(my_dict)

{**my_dict, **another_dict}

{key: value for key,value in my_dict.items() if key==3}

conversation = {}
conversation.setdefault("messages", []).append("Hello")
conversation.setdefault("message", [1,2,3]).append("HI")
conversation.setdefault("message", [1,2,3]).append("HI1")

{**conversation, **my_dict}

from collections import defaultdict
token_counts = defaultdict(int)  # Default value is 0
token_counts["the"] += 1  # No KeyError!

from collections import Counter
token_counts = Counter(conversation)  # Automatic counting


# The "Manual" Approach
text = "system design interview system design coding interview"
words = text.split()

counts = {}
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1

print(counts)
# Output: {'system': 2, 'design': 2, 'interview': 2, 'coding': 1}

from collections import Counter
print(Counter(words))


user_response = {
    "id": 8492,
    "profile": {
        "name": "Sarah",
        "account_type": "premium"
        # Note: "settings" dictionary is missing here!
    }
}

# ❌ The Risky Line:
# We want to get the theme, defaulting to "light" if missing.
theme = user_response["profile"].get("settings", {}).get("theme", "light")



results = [
    {"model": "GPT-4", "score": 88},
    {"model": "Claude", "score": 85},
    {"model": "GPT-4", "score": 94},
    {"model": "Claude", "score": 89},
    {"model": "GPT-4", "score": 91}
]

from collections import defaultdict
group_by_models = defaultdict(list)

for result in results:
    model_name = result["model"]
    group_by_models[model_name].append(result["score"])


models_avg_score = {model: sum(scores) / len(scores) for model, scores in group_by_models.items()}
# models_avg_score = {'GPT-4': 91.0, 'Claude': 87.0}

max(models_avg_score, key= lambda x: models_avg_score[x])

scores = {'GPT-4': 90, 'Claude': 90, 'Llama': 85}

group_by_scores = defaultdict(list)

for model, score in scores.items():
    group_by_scores[score].append(model)


transactions = [
    {"id": 101, "status": "completed", "amount": 50.0},
    {"id": 102, "amount": 25.0},  # ⚠️ Missing status!
    {"id": 103, "status": "completed", "amount": 30.0},
    {"id": 104, "status": "refunded", "amount": 10.0},
    {"id": 105, "status": "completed", "amount": 20.0},
]

group_by_status = defaultdict(int)
for trans in transactions:
    transaction_status = trans.get("status", "pending")
    group_by_status[transaction_status] += trans["amount"]



from collections import defaultdict
supplier_a = [{"product": "Apple", "count": 10}, {"product": "Banana", "count": 5}]
supplier_b = [{"product": "Orange", "count": 8}, {"product": "Apple", "count": 15}]

all_items = supplier_a + supplier_b

merged_products = defaultdict(int)

for items in all_items:
    merged_products[items["product"]] += items["count"]
    



logs = [
    {"date": "2023-01-01", "user": "alice", "action": "login"},
    {"date": "2023-01-01", "user": "alice", "action": "click"},
    {"date": "2023-01-01", "user": "bob",   "action": "login"},
    {"date": "2023-01-02", "user": "alice", "action": "logout"},
]

group_by_data_user = defaultdict(int)

for log in logs:
    data = log["date"]
    user = log["user"]

    group_by_data_user[(data, user)] += 1


logs = [
    {"date": "2023-01-01", "user": "alice", "action": "login"},
    {"date": "2023-01-01", "user": "alice", "action": "click"},
    {"date": "2023-01-01", "user": "bob",   "action": "login"},
    {"date": "2023-01-02", "user": "alice", "action": "logout"},
]


from collections import Counter
group_by_date = defaultdict(Counter)


for log in logs:
    date = log["date"]
    user = log["user"]
    group_by_date[date][user] += 1

print(group_by_date)
    #group_by_count[user]+=1


from collections import OrderedDict

class LRUCache(OrderedDict):
    def __init__(self, capacity: int):
        self.capacity = capacity
        # We inherit from OrderedDict, so 'self' IS the dictionary.

    def get(self, key: int) -> int:
        # TODO: Return value if exists, else -1.
        # Don't forget to mark it as "recently used"!
        if key not in self:
            return -1
        
        return key

    def put(self, key: int, value: int) -> None:
        # TODO: Add or update key.
        # Check capacity. If full, evict the oldest.
        pass

# Test Case
# cache = LRUCache(2)
# cache.put(1, 1)
# cache.put(2, 2)
# print(cache.get(1))       # Returns 1 (Cache is now [2, 1])
# cache.put(3, 3)           # Evicts 2 (Cache is now [1, 3])
# print(cache.get(2))       # Returns -1 (not found)







