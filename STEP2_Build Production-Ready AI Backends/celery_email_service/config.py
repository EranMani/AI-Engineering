from dotenv import load_dotenv
import os

load_dotenv()

def get_redis_url() -> str:
    url = os.getenv("REDIS_URL")
    if not url:
        raise ValueError("REDIS_URL env key is missing!")
    return url