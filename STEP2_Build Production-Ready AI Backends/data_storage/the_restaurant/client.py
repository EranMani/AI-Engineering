import requests

BASE_URL = "http://127.0.0.1:8000"

def run_app():
    print("CLIENT APP STARTED")

    user_name = input("Enter your username: ")
    my_user_id = None

    print(f"Sending request to create user {user_name}...")
    response = requests.post(f"{BASE_URL}/users/", json={"name": user_name})

    if response.status_code == 200:
        data = response.json()
        # capture the ID from server response
        my_user_id = data["user_id"]
        print(f"Success! you are user id: {my_user_id}")
    elif response.status_code == 400:
        # failure. user exists. lets log in instead
        print("User already exists!. Logging in...")

        login_response = requests.get(f"{BASE_URL}/users/name/{user_name}")
        print(login_response)
        if login_response.status_code == 200:
            data = login_response.json()
            my_user_id = data["user_id"]
            print(f"Logged in succesfully with user ID: {my_user_id}")
    else:
        print(f"Error: {response.text}")
        return

    if my_user_id:
        # create post
        post_title = input("\nWrite a new post title: ")

        print(f"Posting '{post_title}' as User ID {my_user_id}...")

        # inject the user_id captured earlier
        post_payload = {
            "title": post_title,
            "user_id": my_user_id
        }

        response = requests.post(f"{BASE_URL}/posts/", json=post_payload)

        if response.status_code == 200:
            print("✅ Post created successfully!")
            print("Server Response:", response.json())
        else:
            print("❌ Failed to create post.")

if __name__ == "__main__":
    run_app()
