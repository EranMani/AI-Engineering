from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import get_jwt_secret, get_jwt_algorithm, get_jwt_expiration
from schemas import UserCreate, UserLogin, Token, UserResponse

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme - tells FastAPI where to get the token from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# In-memory user storage (in production, use a database)
users_db: Dict[str, Dict] = {}

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    Never store plain text passwords!
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Returns True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary to encode in token (usually contains user_id)
        expires_delta: Optional expiration time override
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=get_jwt_expiration())
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_jwt_secret(),
        algorithm=get_jwt_algorithm()
    )
    return encoded_jwt

def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user from database by username"""
    return users_db.get(username)

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user from database by user_id"""
    for user in users_db.values():
        if user["id"] == user_id:
            return user
    return None

def create_user(user_data: UserCreate) -> Dict:
    """
    Create a new user.
    Hashes the password before storing.
    """
    # Check if user already exists
    if user_data.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create user
    user_id = str(len(users_db) + 1)
    hashed_password = get_password_hash(user_data.password)
    
    user = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    users_db[user_data.username] = user
    return user

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user by checking username and password.
    Returns user dict if valid, None otherwise.
    """
    user = get_user_by_username(username)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    FastAPI dependency to get the current authenticated user.
    This is used in protected routes.
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user: Dict = Depends(get_current_user)):
            return {"user": current_user}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=[get_jwt_algorithm()]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user

# ===== Authentication Endpoints =====

from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user.
    Creates user account and returns user information.
    """
    user = create_user(user_data)
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=user["created_at"]
    )

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint (OAuth2 password flow).
    Returns JWT access token.
    
    Note: OAuth2PasswordRequestForm expects 'username' and 'password' fields.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user_id in payload
    access_token = create_access_token(data={"sub": user["id"]})
    return Token(access_token=access_token)

@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    Protected route - requires valid JWT token.
    """
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        created_at=current_user["created_at"]
    )