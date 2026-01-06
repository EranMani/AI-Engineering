import requests
import json

# The URL where the server is listening
url = "http://127.0.0.1:8000/api/v1/event-handler"

# The payload (The data)
# this mimics waht a user or another system will send to the server
payload = {
    "event_id": "evt_1055",
    "event_type": "user_prompt",
    "data": {
        "prompt": "Explain quantum physics like im 5",
        "model": "gpt-4",
        "temperature": 0.7
    }
}

# Headers
# good practice to specify we are sending JSON
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload, headers=headers)

    # check the result
    if response.status_code == 200:
        print("SUCCESS!")
        print("Server Response: ", response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print("Error details: ", response.text)

except requests. exceptions.ConnectionError:
    print("Error: Could not connect to server. Is uvicorn running?")