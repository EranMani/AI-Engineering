from dotenv import load_dotenv
from pathlib import Path
import os

# Load env variables from .env file
load_dotenv()

def get_redis_url() -> str:
    """Get Redis URL from env variables"""
    url = os.getenv("REDIS_URL")
    if not url:
        raise ValueError("REDIS_URL not found in environment variables!")
    return url

def get_jwt_secret() -> str:
    """Get JWT secret key from environmant variables.
    Used to sign and verify JWT tokens
    """
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise ValueError("JWT_SECRET_KEY not found in environment variables!")
    return secret

def get_jwt_algorithm() -> str:
    """
    Get JWT algorithm. Defaults to HS256 if not specified.
    """
    return os.getenv("JWT_ALGORITHM", "HS256")

def get_jwt_expiration() -> int:
    """
    Get JWT token expiration time in hours.
    Defaults to 24 hours.
    """
    return int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

def get_upload_dir() -> Path:
    """Get the directory for uploaded files.
    Creates the directory if doesnt exists
    """
    upload_dir = Path(os.getenv("UPLOAD_DIR", "uploads"))
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def get_max_file_size() -> int:
    """Get maxiumu file size in bytes.
    Defaults to 10MB (10 * 1024 * 1024)
    """
    return int(os.getenv("MAX_FILE_SIZE", str(10* 1024 * 1024)))