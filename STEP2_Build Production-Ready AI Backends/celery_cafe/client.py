import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

# Pointing to the router structure defined in router.py
BASE_URL = "http://127.0.0.1:8000/api/v1/cafe"

def simulate_customer(name, coffee_type):
    print(f"[{name}] 🚶 Entering cafe...")

    try:
        response = requests.post(f"{BASE_URL}/order", json={
            "customer_name": name,
            "coffee_type": coffee_type
        })

        response.raise_for_status()
        data = response.json()
        task_id = data["task_id"]
        print(f"[{name}] 🎫 Order placed! Ticket: {task_id[:5]}...")
    except Exception as e:
        print(f"[{name}] ❌ Failed to order: {e}")
        return

    status = "PENDING"
    while status not in ["SUCCESS", "FAILURE"]:
        time.sleep(random.uniform(1.5, 3))

        r = requests.get(f"{BASE_URL}/status/{task_id}")
        res_data = r.json()
        status = res_data["status"]

        display_msg = status
        if isinstance(res_data.get("result"), dict):
            progress = res_data["result"].get("progress", "")
            display_msg = f"{status} {progress}"
        elif status == "FAILURE":
            error_info = res_data.get("result") or res_data.get("error", "Unknown error")
            display_msg = f"{status} - {error_info}"

        print(f"[{name}] 🗣️  Status: {display_msg}")

        if status == "SUCCESS":
            print(f"[{name}] 😋 RECEIVED: {res_data.get('result')}")

customers = [
    ("Alice", "Latte"), ("Bob", "Espresso"), ("Charlie", "Cappuccino"),
    ("Dave", "Americano"), ("Eve", "Mocha")
]

with ThreadPoolExecutor(max_workers=5) as executor:
    for name, coffee in customers:
        executor.submit(simulate_customer, name, coffee)