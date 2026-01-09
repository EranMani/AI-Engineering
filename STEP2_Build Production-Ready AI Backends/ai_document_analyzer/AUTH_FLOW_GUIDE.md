# Authentication Flow Guide - Complete Breakdown of auth.py

## Table of Contents
1. [Overview](#overview)
2. [Libraries and Dependencies](#libraries-and-dependencies)
3. [Core Concepts](#core-concepts)
4. [Code Structure Overview](#code-structure-overview)
5. [Stage-by-Stage Flow](#stage-by-stage-flow)
6. [Complete Authentication Flows](#complete-authentication-flows)
7. [How Everything Connects](#how-everything-connects)
8. [Security Considerations](#security-considerations)

---

## Overview

The `auth.py` file implements a complete authentication system using:
- **OAuth2 Password Flow** for login
- **JWT (JSON Web Tokens)** for stateless authentication
- **bcrypt** for secure password hashing
- **FastAPI dependencies** for route protection

This guide breaks down every component, how they work, and how they connect together.

---

## Libraries and Dependencies

### 1. `jose` - JWT Token Handling

**What it does:** Handles creation, encoding, decoding, and verification of JWT tokens.

**Key imports:**
```python
from jose import JWTError, jwt
```

**Components:**
- `jwt.encode()` - Creates and signs JWT tokens
- `jwt.decode()` - Verifies and decodes JWT tokens
- `JWTError` - Exception raised when token is invalid/expired

**Why it's used:**
- Industry-standard JWT library
- Secure token creation and verification
- Handles token expiration automatically

### 2. `passlib` - Password Hashing

**What it does:** Provides secure password hashing and verification.

**Key imports:**
```python
from passlib.context import CryptContext
```

**Components:**
- `CryptContext` - Context manager for password hashing schemes
- `pwd_context.hash()` - Hashes passwords using bcrypt
- `pwd_context.verify()` - Verifies passwords against hashes

**Why it's used:**
- Never store plain text passwords
- bcrypt is cryptographically secure
- Slow by design (prevents brute force attacks)

### 3. `fastapi` - Web Framework Components

**What it does:** Provides web framework functionality for authentication.

**Key imports:**
```python
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
```

**Components:**
- `Depends()` - Dependency injection system
- `HTTPException` - HTTP error responses
- `status` - HTTP status codes
- `APIRouter` - Route organization
- `OAuth2PasswordBearer` - OAuth2 token extraction
- `OAuth2PasswordRequestForm` - OAuth2 login form handling

**Why it's used:**
- Built-in OAuth2 support
- Dependency injection for route protection
- Type-safe HTTP responses

### 4. Standard Library Modules

**`datetime` and `timedelta`:**
- Handle token expiration times
- Track user creation timestamps

**`typing`:**
- Type hints for better code clarity
- `Optional`, `Dict` for type safety

---

## Core Concepts

### 1. OAuth2 Password Flow

**What it is:** A standard authentication flow where:
1. User provides username and password
2. Server validates credentials
3. Server returns an access token
4. Client uses token for subsequent requests

**Why use it:**
- Industry standard
- Secure (passwords sent over HTTPS)
- Stateless (no server-side sessions)

### 2. JWT (JSON Web Tokens)

**What it is:** A compact, URL-safe token format containing:
- **Header:** Algorithm and token type
- **Payload:** Claims (user_id, expiration, etc.)
- **Signature:** Ensures token hasn't been tampered with

**Structure:**
```
header.payload.signature
```

**Example payload:**
```json
{
  "sub": "user_id_123",
  "exp": 1234567890
}
```

**Why use it:**
- Stateless (no database lookups needed)
- Self-contained (all info in token)
- Scalable (works across multiple servers)

### 3. Password Hashing

**What it is:** One-way encryption of passwords.

**Process:**
1. User creates password: `"mypassword123"`
2. System hashes it: `"$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY"`
3. Store hash, never store plain password
4. On login, hash the provided password and compare

**Why hash:**
- Even if database is compromised, passwords are safe
- bcrypt is slow (prevents brute force)
- One-way (can't reverse to get original password)

### 4. Dependency Injection

**What it is:** FastAPI's way of automatically providing dependencies to routes.

**How it works:**
```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # This function runs automatically before protected routes
    return user

@router.get("/protected")
async def protected_route(current_user: Dict = Depends(get_current_user)):
    # get_current_user() is called automatically
    # current_user is the return value
    return {"data": "secret"}
```

**Why use it:**
- Reusable authentication logic
- Automatic token extraction
- Clean route code

---

## Code Structure Overview

The `auth.py` file is organized into sections:

```
1. Imports and Setup
   ├── Library imports
   ├── Password hashing context
   ├── OAuth2 scheme
   └── User storage

2. Password Functions
   ├── get_password_hash()
   └── verify_password()

3. Token Functions
   └── create_access_token()

4. User Database Functions
   ├── get_user_by_username()
   ├── get_user_by_id()
   └── create_user()

5. Authentication Functions
   ├── authenticate_user()
   └── get_current_user() [Dependency]

6. API Endpoints
   ├── POST /register
   ├── POST /login
   └── GET /me
```

---

## Stage-by-Stage Flow

### Stage 1: Initialization and Setup

**Location:** Lines 1-17

**What happens:**

```python
# 1. Import all necessary libraries
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import get_jwt_secret, get_jwt_algorithm, get_jwt_expiration
from schemas import UserCreate, UserLogin, Token, UserResponse
```

**Purpose:** Import all required functionality.

---

```python
# 2. Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**What this does:**
- Creates a context for password operations
- Uses `bcrypt` algorithm (very secure)
- `deprecated="auto"` handles algorithm migrations

**Why:** Centralized password hashing configuration.

---

```python
# 3. Setup OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
```

**What this does:**
- Tells FastAPI where to find tokens
- Extracts tokens from `Authorization: Bearer <token>` header
- `tokenUrl` is used for API documentation

**How it works:**
1. Client sends: `Authorization: Bearer eyJhbGc...`
2. `oauth2_scheme` extracts: `eyJhbGc...`
3. Passes token to dependency functions

**Why:** Automatic token extraction from requests.

---

```python
# 4. In-memory user storage
users_db: Dict[str, Dict] = {}
```

**What this does:**
- Stores users in memory (dictionary)
- Key: username
- Value: user dictionary with id, email, hashed_password, etc.

**Note:** In production, use a real database (PostgreSQL, MongoDB, etc.)

---

### Stage 2: Password Hashing Functions

**Location:** Lines 19-31

#### Function: `get_password_hash()`

```python
def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    Never store plain text passwords!
    """
    return pwd_context.hash(password)
```

**What it does:**
1. Takes plain text password: `"mypassword123"`
2. Hashes it using bcrypt: `"$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY"`
3. Returns the hash

**Example:**
```python
hash = get_password_hash("mypassword123")
# Returns: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY"
```

**When used:** During user registration.

**Why:** Passwords must be hashed before storage.

---

#### Function: `verify_password()`

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Returns True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
```

**What it does:**
1. Takes plain password and stored hash
2. Hashes the plain password
3. Compares with stored hash
4. Returns `True` if match, `False` otherwise

**Example:**
```python
is_valid = verify_password("mypassword123", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY")
# Returns: True

is_valid = verify_password("wrongpassword", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY")
# Returns: False
```

**When used:** During user login.

**Why:** Verify user credentials without storing plain passwords.

---

### Stage 3: JWT Token Creation

**Location:** Lines 33-57

#### Function: `create_access_token()`

```python
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
```

**Step-by-step breakdown:**

1. **Copy data:**
   ```python
   to_encode = data.copy()
   ```
   - Creates a copy to avoid modifying original
   - Example: `{"sub": "user_123"}`

2. **Calculate expiration:**
   ```python
   if expires_delta:
       expire = datetime.utcnow() + expires_delta
   else:
       expire = datetime.utcnow() + timedelta(hours=get_jwt_expiration())
   ```
   - If custom expiration provided, use it
   - Otherwise, use default from config (24 hours)
   - Example: `2024-01-02 12:00:00`

3. **Add expiration to payload:**
   ```python
   to_encode.update({"exp": expire})
   ```
   - Adds `exp` claim (standard JWT claim)
   - Token will be invalid after this time
   - Example: `{"sub": "user_123", "exp": 2024-01-02 12:00:00}`

4. **Encode token:**
   ```python
   encoded_jwt = jwt.encode(
       to_encode,
       get_jwt_secret(),
       algorithm=get_jwt_algorithm()
   )
   ```
   - Encodes payload with secret key
   - Signs token (prevents tampering)
   - Returns: `"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTcwNDE..."`

**Example usage:**
```python
token = create_access_token(data={"sub": "user_123"})
# Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**When used:** After successful login.

**Why:** Provides stateless authentication token.

---

### Stage 4: User Database Functions

**Location:** Lines 59-103

#### Function: `get_user_by_username()`

```python
def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user from database by username"""
    return users_db.get(username)
```

**What it does:**
- Looks up user in `users_db` dictionary
- Returns user dict if found, `None` otherwise

**Example:**
```python
user = get_user_by_username("alice")
# Returns: {"id": "1", "username": "alice", "email": "alice@example.com", ...}
# Or: None if not found
```

**When used:** During login and registration checks.

---

#### Function: `get_user_by_id()`

```python
def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user from database by user_id"""
    for user in users_db.values():
        if user["id"] == user_id:
            return user
    return None
```

**What it does:**
- Searches all users for matching `user_id`
- Returns user dict if found, `None` otherwise

**Example:**
```python
user = get_user_by_id("1")
# Returns: {"id": "1", "username": "alice", ...}
```

**When used:** During token verification (to get user from token's user_id).

---

#### Function: `create_user()`

```python
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
```

**Step-by-step breakdown:**

1. **Check username uniqueness:**
   ```python
   if user_data.username in users_db:
       raise HTTPException(...)
   ```
   - Prevents duplicate usernames
   - Returns 400 error if exists

2. **Check email uniqueness:**
   ```python
   for user in users_db.values():
       if user["email"] == user_data.email:
           raise HTTPException(...)
   ```
   - Prevents duplicate emails
   - Returns 400 error if exists

3. **Generate user ID:**
   ```python
   user_id = str(len(users_db) + 1)
   ```
   - Simple incrementing ID
   - In production, use UUID

4. **Hash password:**
   ```python
   hashed_password = get_password_hash(user_data.password)
   ```
   - Never store plain password!
   - Uses bcrypt hashing

5. **Create user object:**
   ```python
   user = {
       "id": user_id,
       "username": user_data.username,
       "email": user_data.email,
       "hashed_password": hashed_password,
       "created_at": datetime.utcnow()
   }
   ```
   - All user data in one dict
   - Timestamp for audit trail

6. **Store user:**
   ```python
   users_db[user_data.username] = user
   return user
   ```
   - Saves to in-memory database
   - Returns created user

**When used:** During user registration.

**Why:** Centralized user creation with validation.

---

### Stage 5: Authentication Functions

**Location:** Lines 105-153

#### Function: `authenticate_user()`

```python
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
```

**Step-by-step breakdown:**

1. **Look up user:**
   ```python
   user = get_user_by_username(username)
   if not user:
       return None
   ```
   - Finds user by username
   - Returns `None` if not found

2. **Verify password:**
   ```python
   if not verify_password(password, user["hashed_password"]):
       return None
   ```
   - Compares provided password with stored hash
   - Returns `None` if password doesn't match

3. **Return user:**
   ```python
   return user
   ```
   - Returns user dict if authentication successful

**Example:**
```python
user = authenticate_user("alice", "correctpassword")
# Returns: {"id": "1", "username": "alice", ...}

user = authenticate_user("alice", "wrongpassword")
# Returns: None
```

**When used:** During login.

**Why:** Validates user credentials.

---

#### Function: `get_current_user()` - The Dependency

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    FastAPI dependency to get the current authenticated user.
    This is used in protected routes.
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
```

**This is the most important function!** It's a FastAPI dependency that automatically runs before protected routes.

**Step-by-step breakdown:**

1. **Define error response:**
   ```python
   credentials_exception = HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail="Could not validate credentials",
       headers={"WWW-Authenticate": "Bearer"},
   )
   ```
   - Standard 401 Unauthorized error
   - `WWW-Authenticate` header tells client to use Bearer token

2. **Extract token (automatic):**
   ```python
   token: str = Depends(oauth2_scheme)
   ```
   - FastAPI automatically extracts token from `Authorization` header
   - `oauth2_scheme` handles the extraction
   - No manual work needed!

3. **Decode and verify token:**
   ```python
   try:
       payload = jwt.decode(
           token,
           get_jwt_secret(),
           algorithms=[get_jwt_algorithm()]
       )
   except JWTError:
       raise credentials_exception
   ```
   - `jwt.decode()` verifies:
     - Token signature (not tampered)
     - Token expiration (not expired)
     - Algorithm matches
   - Raises `JWTError` if invalid
   - Returns payload if valid

4. **Extract user_id:**
   ```python
   user_id: str = payload.get("sub")
   if user_id is None:
       raise credentials_exception
   ```
   - `sub` (subject) claim contains user_id
   - Standard JWT claim name
   - Raises error if missing

5. **Get user from database:**
   ```python
   user = get_user_by_id(user_id)
   if user is None:
       raise credentials_exception
   ```
   - Looks up user by ID
   - Raises error if user doesn't exist (maybe deleted)

6. **Return user:**
   ```python
   return user
   ```
   - Returns user dict
   - Available in route as `current_user` parameter

**How it's used in routes:**
```python
@router.get("/protected")
async def protected_route(current_user: Dict = Depends(get_current_user)):
    # get_current_user() runs automatically
    # current_user contains the authenticated user
    return {"user_id": current_user["id"]}
```

**When used:** Automatically on every protected route.

**Why:** Reusable authentication logic, clean route code.

---

### Stage 6: API Endpoints

**Location:** Lines 155-206

#### Endpoint: `POST /register`

```python
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
```

**Flow:**
1. Client sends POST request with `UserCreate` data
2. FastAPI validates data against `UserCreate` schema
3. `create_user()` is called:
   - Validates uniqueness
   - Hashes password
   - Creates user record
4. Returns `UserResponse` (without password!)

**Request example:**
```json
POST /api/v1/auth/register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "securepassword123"
}
```

**Response example:**
```json
{
  "id": "1",
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

**Note:** Password is never returned in response!

---

#### Endpoint: `POST /login`

```python
@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint (OAuth2 password flow).
    Returns JWT access token.
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
```

**Flow:**
1. Client sends POST request with username/password
2. `OAuth2PasswordRequestForm` extracts form data
3. `authenticate_user()` validates credentials
4. If invalid, returns 401 error
5. If valid, creates JWT token with user_id
6. Returns token

**Request example:**
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=alice&password=securepassword123
```

**Note:** OAuth2 uses form data, not JSON!

**Response example:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Client then uses token:**
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

#### Endpoint: `GET /me`

```python
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
```

**Flow:**
1. Client sends GET request with `Authorization: Bearer <token>` header
2. `get_current_user()` dependency runs automatically:
   - Extracts token from header
   - Verifies token
   - Gets user from database
3. Returns user information

**Request example:**
```bash
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response example:**
```json
{
  "id": "1",
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

**Why protected:** Only authenticated users can see their own info.

---

## Complete Authentication Flows

### Flow 1: User Registration

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     │ 1. POST /register
     │    {username, email, password}
     ▼
┌─────────────────┐
│  FastAPI Route  │
│  /register      │
└────┬────────────┘
     │
     │ 2. Validate UserCreate schema
     ▼
┌──────────────┐
│ create_user()│
└────┬─────────┘
     │
     │ 3. Check username/email uniqueness
     │ 4. Hash password (get_password_hash)
     │ 5. Create user record
     │ 6. Store in users_db
     ▼
┌──────────────┐
│ UserResponse │
└────┬─────────┘
     │
     │ 7. Return user info (no password!)
     ▼
┌─────────┐
│ Client  │
└─────────┘
```

**Steps:**
1. Client sends registration data
2. FastAPI validates schema
3. `create_user()` checks uniqueness
4. Password is hashed
5. User record created
6. Stored in database
7. User info returned (password excluded)

---

### Flow 2: User Login

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     │ 1. POST /login
     │    username + password (form data)
     ▼
┌─────────────────┐
│  FastAPI Route  │
│  /login         │
└────┬────────────┘
     │
     │ 2. OAuth2PasswordRequestForm extracts data
     ▼
┌──────────────────┐
│authenticate_user()│
└────┬──────────────┘
     │
     │ 3. get_user_by_username()
     │ 4. verify_password()
     │ 5. Return user if valid
     ▼
┌──────────────────┐
│create_access_token()│
└────┬──────────────┘
     │
     │ 6. Create JWT with user_id
     │ 7. Sign with secret key
     │ 8. Add expiration
     ▼
┌──────────────┐
│ Token        │
│ {access_token}│
└────┬─────────┘
     │
     │ 9. Return token
     ▼
┌─────────┐
│ Client  │
└─────────┘
```

**Steps:**
1. Client sends credentials
2. FastAPI extracts form data
3. Look up user by username
4. Verify password against hash
5. Return user if valid
6. Create JWT token with user_id
7. Sign token with secret
8. Add expiration time
9. Return token to client

---

### Flow 3: Accessing Protected Route

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     │ 1. GET /protected
     │    Authorization: Bearer <token>
     ▼
┌─────────────────┐
│  FastAPI Route  │
│  /protected     │
└────┬────────────┘
     │
     │ 2. get_current_user() dependency runs
     ▼
┌──────────────────┐
│ oauth2_scheme    │
└────┬─────────────┘
     │
     │ 3. Extract token from header
     ▼
┌──────────────────┐
│ jwt.decode()     │
└────┬─────────────┘
     │
     │ 4. Verify signature
     │ 5. Check expiration
     │ 6. Extract user_id from payload
     ▼
┌──────────────────┐
│ get_user_by_id() │
└────┬─────────────┘
     │
     │ 7. Look up user
     ▼
┌──────────────────┐
│ Return user dict │
└────┬─────────────┘
     │
     │ 8. Pass to route as current_user
     ▼
┌─────────────────┐
│  Route Handler  │
│  (has access to │
│   current_user) │
└────┬────────────┘
     │
     │ 9. Process request
     │ 10. Return response
     ▼
┌─────────┐
│ Client  │
└─────────┘
```

**Steps:**
1. Client sends request with Bearer token
2. FastAPI dependency system activates
3. `oauth2_scheme` extracts token from header
4. `jwt.decode()` verifies token signature
5. Checks if token is expired
6. Extracts `user_id` from payload
7. Looks up user in database
8. Returns user to route
9. Route processes request with user context
10. Returns response

---

## How Everything Connects

### Connection Map

```
┌─────────────────────────────────────────────────────────┐
│                    auth.py Module                         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Libraries  │────────▶│   Setup      │             │
│  │              │         │              │             │
│  │ - jose       │         │ - pwd_context│             │
│  │ - passlib    │         │ - oauth2_scheme│           │
│  │ - fastapi    │         │ - users_db   │             │
│  └──────────────┘         └──────────────┘             │
│         │                        │                       │
│         │                        │                       │
│         ▼                        ▼                       │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Password   │         │     Token    │             │
│  │   Functions  │         │   Functions  │             │
│  │              │         │              │             │
│  │ - hash()     │         │ - create()   │             │
│  │ - verify()   │         │              │             │
│  └──────────────┘         └──────────────┘             │
│         │                        │                       │
│         │                        │                       │
│         ▼                        ▼                       │
│  ┌──────────────┐         ┌──────────────┐             │
│  │     User     │         │ Authentication│            │
│  │   Database   │         │   Functions  │            │
│  │   Functions  │         │              │             │
│  │              │         │ - authenticate│             │
│  │ - get_by_*() │         │ - get_current │            │
│  │ - create()   │         │              │             │
│  └──────────────┘         └──────────────┘             │
│         │                        │                       │
│         │                        │                       │
│         └──────────┬─────────────┘                       │
│                    │                                       │
│                    ▼                                       │
│         ┌──────────────────┐                              │
│         │  API Endpoints   │                              │
│         │                  │                              │
│         │ - /register      │                              │
│         │ - /login         │                              │
│         │ - /me            │                              │
│         └──────────────────┘                              │
│                                                           │
└─────────────────────────────────────────────────────────┘
         │
         │ Uses
         ▼
┌─────────────────────────────────────────────────────────┐
│              External Dependencies                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   config.py  │         │  schemas.py   │             │
│  │              │         │              │             │
│  │ - JWT secret │         │ - UserCreate │             │
│  │ - Algorithm  │         │ - Token      │             │
│  │ - Expiration │         │ - UserResponse│            │
│  └──────────────┘         └──────────────┘             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Data Flow Example: Complete Login Flow

```
1. Client Request
   ↓
   POST /api/v1/auth/login
   username=alice&password=secret123
   
2. FastAPI Receives
   ↓
   OAuth2PasswordRequestForm extracts:
   - form_data.username = "alice"
   - form_data.password = "secret123"
   
3. Authentication
   ↓
   authenticate_user("alice", "secret123")
   ├─→ get_user_by_username("alice")
   │   └─→ Returns: {"id": "1", "hashed_password": "$2b$12$..."}
   │
   └─→ verify_password("secret123", "$2b$12$...")
       └─→ Returns: True
   
4. Token Creation
   ↓
   create_access_token(data={"sub": "1"})
   ├─→ Add expiration: {"sub": "1", "exp": 2024-01-02 12:00:00}
   ├─→ jwt.encode(payload, secret, algorithm)
   └─→ Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   
5. Response
   ↓
   Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
   └─→ JSON: {"access_token": "...", "token_type": "bearer"}
```

### Dependency Injection Flow

```
Route Definition:
@router.get("/protected")
async def route(current_user: Dict = Depends(get_current_user)):
    return current_user

When Route is Called:
1. FastAPI sees Depends(get_current_user)
2. Calls get_current_user() first
3. get_current_user() needs token
4. Calls Depends(oauth2_scheme) to get token
5. oauth2_scheme extracts from Authorization header
6. Returns token to get_current_user()
7. get_current_user() verifies token
8. Returns user dict
9. FastAPI passes user dict as current_user parameter
10. Route handler executes with current_user available
```

---

## Security Considerations

### 1. Password Security

**What's secure:**
- ✅ Passwords are hashed with bcrypt (one-way)
- ✅ Never stored in plain text
- ✅ Slow hashing prevents brute force

**What to improve:**
- Use stronger password requirements
- Implement password reset flow
- Add rate limiting on login attempts

### 2. Token Security

**What's secure:**
- ✅ Tokens are signed (can't be tampered)
- ✅ Tokens expire (limited lifetime)
- ✅ Secret key stored in environment

**What to improve:**
- Use HTTPS in production (tokens in headers)
- Implement token refresh mechanism
- Add token revocation (blacklist)

### 3. Storage Security

**Current:**
- ⚠️ In-memory storage (lost on restart)
- ⚠️ No persistence

**Production:**
- Use real database (PostgreSQL, MongoDB)
- Encrypt sensitive data
- Regular backups

### 4. Best Practices

**Do:**
- ✅ Always hash passwords
- ✅ Use HTTPS in production
- ✅ Validate all inputs
- ✅ Handle errors gracefully
- ✅ Use environment variables for secrets

**Don't:**
- ❌ Store plain text passwords
- ❌ Log passwords or tokens
- ❌ Use weak secret keys
- ❌ Skip input validation

---

## Summary

The `auth.py` file implements a complete, production-ready authentication system:

1. **Password Hashing:** Secure bcrypt hashing
2. **JWT Tokens:** Stateless authentication
3. **OAuth2 Flow:** Industry-standard login
4. **Dependency Injection:** Reusable route protection
5. **User Management:** Create, authenticate, retrieve users

**Key Takeaways:**
- Passwords are never stored in plain text
- Tokens provide stateless authentication
- Dependencies make route protection easy
- OAuth2 is the standard for API authentication
- All components work together seamlessly

This system can be extended with:
- Token refresh
- Password reset
- Email verification
- Two-factor authentication
- Role-based access control

---

**Happy Authenticating! 🔐**

