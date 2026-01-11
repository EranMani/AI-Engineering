import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1/email"

def test_send_email():
    response = requests.post(f"{BASE_URL}/send_email", json={
        "to": "eranmani@gmail.com",
        "subject": "This is a test email",
        "body": "This is a test email"
    })

    task_id = response.json()["task_id"]
    print(task_id)

    while True:
        status_response = requests.get(f"{BASE_URL}/check_status/{task_id}")
        status_data = status_response.json()

        current_status = status_data["status"]

        if current_status == "SUCCESS":
            print("Mail was successfuly sent!")
            break
        elif current_status == "FAILURE":
            print("Mail has been failed!")
            break


        time.sleep(3)




if __name__ == "__main__":
    for i in range(140):
        test_send_email()