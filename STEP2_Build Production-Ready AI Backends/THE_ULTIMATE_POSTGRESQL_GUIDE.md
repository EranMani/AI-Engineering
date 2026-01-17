# The Ultimate PostgreSQL Guide for Beginners 🐘

> **Written by a 20-year veteran backend developer**  
> **Comprehension Level: Teenager-friendly**  
> **Goal: Master PostgreSQL from zero to hero**

---

## Table of Contents

1. [What is PostgreSQL?](#what-is-postgresql)
2. [Installing PostgreSQL from Scratch](#installing-postgresql-from-scratch)
3. [Your First Database Connection](#your-first-database-connection)
4. [Understanding Databases, Tables, and Rows](#understanding-databases-tables-and-rows)
5. [Raw SQL Building Blocks](#raw-sql-building-blocks)
6. [Working with Data (CRUD Operations)](#working-with-data-crud-operations)
7. [Relationships and Foreign Keys](#relationships-and-foreign-keys)
8. [Advanced SQL Concepts](#advanced-sql-concepts)
9. [Connecting PostgreSQL with Python](#connecting-postgresql-with-python)
10. [SQLAlchemy: The Python Way to Work with PostgreSQL](#sqlalchemy-the-python-way-to-work-with-postgresql)
11. [Real-World Examples](#real-world-examples)
12. [Best Practices and Security](#best-practices-and-security)
13. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## What is PostgreSQL?

### The Simple Explanation

Imagine you have a **giant filing cabinet** that can store millions of pieces of information. PostgreSQL is like that filing cabinet, but it's:
- **Super fast** at finding information
- **Super organized** with labels and categories
- **Super reliable** - it never loses your data
- **Super smart** - it can connect related information together

### Why PostgreSQL?

PostgreSQL (often called "Postgres") is one of the most popular databases in the world because:
- ✅ It's **free** and open-source
- ✅ It's **powerful** - used by companies like Instagram, Spotify, and Apple
- ✅ It's **reliable** - your data is safe
- ✅ It's **flexible** - works with any programming language

### Real-World Analogy

Think of PostgreSQL like a **library system**:
- **Database** = The entire library building
- **Table** = A bookshelf (e.g., "Fiction Books" shelf)
- **Row** = One book on the shelf
- **Column** = Information about the book (title, author, ISBN)
- **Primary Key** = The unique book ID number
- **Foreign Key** = A reference to another shelf (like "This book belongs to the Sci-Fi section")

---

## Installing PostgreSQL from Scratch

### Step 1: Download PostgreSQL

**For Windows:**
1. Go to https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Download the latest version (e.g., PostgreSQL 16)

**For Mac:**
```bash
# Using Homebrew (recommended)
brew install postgresql@16
brew services start postgresql@16
```

**For Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Install PostgreSQL

**Windows Installation:**
1. Run the installer
2. Choose installation directory (default is fine)
3. **IMPORTANT:** Remember the password you set for the `postgres` user!
4. Port: Keep default `5432`
5. Finish installation

### Step 3: Verify Installation

**Windows:**
- Open "pgAdmin 4" (comes with PostgreSQL)
- Or open Command Prompt and type: `psql --version`

**Mac/Linux:**
```bash
psql --version
# Should show: psql (PostgreSQL) 16.x
```

### Step 4: Start PostgreSQL Service

**Windows:**
- PostgreSQL usually starts automatically
- Check in Services (search "Services" in Windows)

**Mac:**
```bash
brew services start postgresql@16
```

**Linux:**
```bash
sudo systemctl start postgresql
```

---

## Your First Database Connection

### Understanding the Connection String

A connection string tells your program **how to connect** to PostgreSQL:

```
postgresql://username:password@host:port/database_name
```

**Breaking it down:**
- `postgresql://` = Protocol (how to talk to the database)
- `username` = Your PostgreSQL username (default: `postgres`)
- `password` = Your PostgreSQL password
- `host` = Where the database is (usually `localhost` for your computer)
- `port` = The door number (default: `5432`)
- `database_name` = Which database to use

**Example:**
```
postgresql://postgres:mypassword123@localhost:5432/mydb
```

### Connecting via Command Line (psql)

**Windows:**
1. Open Command Prompt
2. Navigate to PostgreSQL bin folder (usually `C:\Program Files\PostgreSQL\16\bin`)
3. Or add it to your PATH
4. Type: `psql -U postgres`

**Mac/Linux:**
```bash
psql -U postgres
```

You'll be prompted for your password. Type it in (you won't see it typing - that's normal for security).

### Your First SQL Command

Once connected, try this:

```sql
-- List all databases
\l

-- Create your first database
CREATE DATABASE my_first_db;

-- Connect to your new database
\c my_first_db

-- See what tables exist (none yet!)
\dt
```

**What just happened?**
- `\l` = List all databases (like showing all library buildings)
- `CREATE DATABASE` = Create a new empty database
- `\c` = Connect to a database (enter the library building)
- `\dt` = Show all tables (show all bookshelves)

---

## Understanding Databases, Tables, and Rows

### The Hierarchy

```
PostgreSQL Server
    └── Database (my_first_db)
        └── Table (users)
            └── Row 1: id=1, name="Alice", email="alice@email.com"
            └── Row 2: id=2, name="Bob", email="bob@email.com"
            └── Row 3: id=3, name="Charlie", email="charlie@email.com"
```

### Creating Your First Table

Let's create a table to store users:

```sql
-- Connect to your database first
\c my_first_db

-- Create a users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Breaking down each part:**

1. **`CREATE TABLE users`** = "Hey PostgreSQL, create a new table called 'users'"

2. **`id SERIAL PRIMARY KEY`**
   - `SERIAL` = Auto-incrementing number (1, 2, 3, 4...)
   - `PRIMARY KEY` = Unique identifier (like a social security number)
   - Every row MUST have a unique ID

3. **`name VARCHAR(100) NOT NULL`**
   - `VARCHAR(100)` = Text up to 100 characters
   - `NOT NULL` = This field is required (can't be empty)

4. **`email VARCHAR(255) UNIQUE NOT NULL`**
   - `VARCHAR(255)` = Text up to 255 characters
   - `UNIQUE` = No two users can have the same email
   - `NOT NULL` = Required field

5. **`age INTEGER`**
   - `INTEGER` = Whole number (no decimals)
   - No `NOT NULL`, so age is optional

6. **`created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`**
   - `TIMESTAMP` = Date and time
   - `DEFAULT CURRENT_TIMESTAMP` = Automatically set to "right now" when row is created

### Viewing Your Table Structure

```sql
-- See the structure of your table
\d users

-- This shows:
-- Column name | Data type | Constraints
```

---

## Raw SQL Building Blocks

### Data Types (The Building Materials)

PostgreSQL has different "containers" for different types of data:

#### Text Types
```sql
VARCHAR(50)      -- Text up to 50 characters
TEXT             -- Unlimited text
CHAR(10)         -- Exactly 10 characters (padded with spaces)
```

#### Number Types
```sql
INTEGER          -- Whole numbers: -2,147,483,648 to 2,147,483,647
BIGINT           -- Really big whole numbers
SMALLINT         -- Small whole numbers: -32,768 to 32,767
DECIMAL(10, 2)   -- Decimal numbers: 10 total digits, 2 after decimal (e.g., 12345678.90)
REAL             -- Floating point number (can have decimals)
DOUBLE PRECISION -- More precise floating point
```

#### Date/Time Types
```sql
DATE             -- Just the date: '2024-01-15'
TIME             -- Just the time: '14:30:00'
TIMESTAMP        -- Date and time: '2024-01-15 14:30:00'
TIMESTAMPTZ      -- Timestamp with timezone
```

#### Boolean Type
```sql
BOOLEAN          -- TRUE or FALSE
```

#### Other Useful Types
```sql
UUID             -- Unique identifier (like: '550e8400-e29b-41d4-a716-446655440000')
JSON             -- Store JSON data
JSONB            -- Binary JSON (faster for queries)
ARRAY            -- List of values: ARRAY['apple', 'banana', 'orange']
```

### Constraints (The Rules)

Constraints are **rules** that your data must follow:

```sql
PRIMARY KEY      -- Unique identifier (one per table)
UNIQUE          -- No duplicates allowed
NOT NULL        -- Field is required
DEFAULT value   -- Use this value if nothing is provided
CHECK (condition) -- Data must meet this condition
FOREIGN KEY     -- References another table (we'll cover this later)
```

**Example with constraints:**
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,                    -- Must be unique
    name VARCHAR(100) NOT NULL,              -- Required
    price DECIMAL(10, 2) CHECK (price > 0),  -- Must be positive
    stock INTEGER DEFAULT 0,                 -- Defaults to 0 if not provided
    sku VARCHAR(50) UNIQUE                   -- No duplicates
);
```

---

## Working with Data (CRUD Operations)

CRUD stands for:
- **C**reate (INSERT)
- **R**ead (SELECT)
- **U**pdate (UPDATE)
- **D**elete (DELETE)

### CREATE: Inserting Data

#### Insert One Row
```sql
-- Basic insert
INSERT INTO users (name, email, age)
VALUES ('Alice', 'alice@email.com', 25);

-- Insert with all fields
INSERT INTO users (name, email, age, created_at)
VALUES ('Bob', 'bob@email.com', 30, '2024-01-15 10:30:00');

-- Insert using defaults (created_at will be automatic)
INSERT INTO users (name, email, age)
VALUES ('Charlie', 'charlie@email.com', 28);
```

#### Insert Multiple Rows at Once
```sql
INSERT INTO users (name, email, age)
VALUES 
    ('David', 'david@email.com', 22),
    ('Eve', 'eve@email.com', 35),
    ('Frank', 'frank@email.com', 29);
```

**What happens:**
- PostgreSQL creates a new row
- Auto-generates the `id` (1, 2, 3...)
- Sets `created_at` to current time (if you didn't specify)

### READ: Selecting Data

#### Select Everything
```sql
-- Get all users
SELECT * FROM users;

-- Result:
-- id | name    | email              | age | created_at
-- 1  | Alice   | alice@email.com    | 25  | 2024-01-15 10:00:00
-- 2  | Bob     | bob@email.com      | 30  | 2024-01-15 10:05:00
```

#### Select Specific Columns
```sql
-- Only get name and email
SELECT name, email FROM users;

-- Result:
-- name    | email
-- Alice   | alice@email.com
-- Bob     | bob@email.com
```

#### Filter with WHERE
```sql
-- Get users older than 25
SELECT * FROM users WHERE age > 25;

-- Get user with specific email
SELECT * FROM users WHERE email = 'alice@email.com';

-- Get users between ages 25 and 30
SELECT * FROM users WHERE age BETWEEN 25 AND 30;

-- Get users with names starting with 'A'
SELECT * FROM users WHERE name LIKE 'A%';

-- Multiple conditions (AND)
SELECT * FROM users WHERE age > 25 AND email LIKE '%@email.com';

-- Multiple conditions (OR)
SELECT * FROM users WHERE age < 20 OR age > 40;
```

**WHERE clause operators:**
- `=` Equal to
- `!=` or `<>` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `BETWEEN` In a range
- `LIKE` Pattern matching (`%` = any characters, `_` = one character)
- `IN` Match any value in a list
- `IS NULL` / `IS NOT NULL` Check for empty values

#### Sorting Results (ORDER BY)
```sql
-- Sort by age (ascending - youngest first)
SELECT * FROM users ORDER BY age ASC;

-- Sort by age (descending - oldest first)
SELECT * FROM users ORDER BY age DESC;

-- Sort by multiple columns
SELECT * FROM users ORDER BY age DESC, name ASC;
-- (Oldest first, then alphabetically by name)
```

#### Limiting Results (LIMIT)
```sql
-- Get only the first 5 users
SELECT * FROM users LIMIT 5;

-- Get 5 users, but skip the first 3 (pagination)
SELECT * FROM users LIMIT 5 OFFSET 3;
```

#### Counting Rows
```sql
-- Count all users
SELECT COUNT(*) FROM users;

-- Count users older than 25
SELECT COUNT(*) FROM users WHERE age > 25;

-- Count with grouping
SELECT age, COUNT(*) FROM users GROUP BY age;
```

### UPDATE: Modifying Data

```sql
-- Update one user's age
UPDATE users 
SET age = 26 
WHERE email = 'alice@email.com';

-- Update multiple fields
UPDATE users 
SET age = 31, name = 'Robert' 
WHERE email = 'bob@email.com';

-- Update multiple rows
UPDATE users 
SET age = age + 1 
WHERE age < 30;
-- (Adds 1 year to everyone under 30)

-- ⚠️ WARNING: Always use WHERE!
-- This updates EVERY row (usually bad!):
UPDATE users SET age = 25;  -- ❌ DANGEROUS!
```

### DELETE: Removing Data

```sql
-- Delete one user
DELETE FROM users WHERE email = 'alice@email.com';

-- Delete multiple users
DELETE FROM users WHERE age < 18;

-- ⚠️ WARNING: Always use WHERE!
-- This deletes EVERYTHING (usually bad!):
DELETE FROM users;  -- ❌ DANGEROUS! Deletes all users!
```

---

## Relationships and Foreign Keys

### Why Relationships Matter

Imagine you're building a **blog system**:
- Users write Posts
- Each Post belongs to one User
- This is a **relationship**

Without relationships, you'd have to copy user information into every post (wasteful and error-prone).

### Understanding Foreign Keys

A **Foreign Key** is like a **reference** or **pointer** to another table.

**Real-world analogy:**
- In a library, a book has a "section_id" that points to which section it belongs to
- The book doesn't contain all the section information
- It just says "I belong to section #5"

### Example: Users and Posts

#### Step 1: Create the Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);
```

#### Step 2: Create the Posts Table with Foreign Key
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**The magic line:**
```sql
user_id INTEGER REFERENCES users(id)
```

This means:
- `user_id` is an integer
- It **references** the `id` column in the `users` table
- PostgreSQL will **enforce** this relationship

#### Step 3: Insert Data with Relationships

```sql
-- First, create users
INSERT INTO users (name, email) VALUES ('Alice', 'alice@email.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@email.com');

-- Now create posts (using the user IDs)
INSERT INTO posts (title, content, user_id) 
VALUES ('My First Post', 'This is my first blog post!', 1);
-- user_id = 1 means this post belongs to Alice

INSERT INTO posts (title, content, user_id) 
VALUES ('Another Post', 'More content here!', 1);
-- Another post by Alice

INSERT INTO posts (title, content, user_id) 
VALUES ('Bob''s Post', 'Hello from Bob!', 2);
-- This post belongs to Bob (user_id = 2)
```

#### Step 4: Query with JOINs

**The Problem:** If you just do `SELECT * FROM posts`, you'll see `user_id = 1`, but not "Alice".

**The Solution:** Use JOIN to combine tables:

```sql
-- Get posts with user information
SELECT 
    posts.title,
    posts.content,
    users.name AS author_name,
    users.email AS author_email
FROM posts
JOIN users ON posts.user_id = users.id;
```

**Result:**
```
title           | content                    | author_name | author_email
My First Post   | This is my first blog...   | Alice       | alice@email.com
Another Post    | More content here!         | Alice       | alice@email.com
Bob's Post      | Hello from Bob!            | Bob         | bob@email.com
```

**How JOIN works:**
1. Start with `posts` table
2. For each post, find the matching user where `posts.user_id = users.id`
3. Combine the data from both tables

#### Types of JOINs

**INNER JOIN** (default - only matching rows):
```sql
SELECT posts.title, users.name
FROM posts
INNER JOIN users ON posts.user_id = users.id;
-- Only shows posts that have a valid user
```

**LEFT JOIN** (all posts, even if user doesn't exist):
```sql
SELECT posts.title, users.name
FROM posts
LEFT JOIN users ON posts.user_id = users.id;
-- Shows all posts, even if user_id is invalid (shows NULL for user.name)
```

**RIGHT JOIN** (all users, even if they have no posts):
```sql
SELECT posts.title, users.name
FROM posts
RIGHT JOIN users ON posts.user_id = users.id;
-- Shows all users, even if they have no posts (shows NULL for post.title)
```

### Real-World Example: E-Commerce System

```sql
-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items (the "many-to-many" relationship)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

**This structure allows:**
- One user can have many orders
- One order can have many products (through order_items)
- One product can be in many orders

**Query to get order details:**
```sql
SELECT 
    users.name AS customer,
    orders.id AS order_id,
    products.name AS product,
    order_items.quantity,
    order_items.price
FROM orders
JOIN users ON orders.user_id = users.id
JOIN order_items ON orders.id = order_items.order_id
JOIN products ON order_items.product_id = products.id
WHERE orders.id = 1;
```

---

## Advanced SQL Concepts

### Aggregation Functions

These functions **summarize** data:

```sql
-- Count
SELECT COUNT(*) FROM users;  -- Total number of users

-- Sum
SELECT SUM(price) FROM products;  -- Total of all prices

-- Average
SELECT AVG(age) FROM users;  -- Average age

-- Minimum
SELECT MIN(price) FROM products;  -- Cheapest product

-- Maximum
SELECT MAX(price) FROM products;  -- Most expensive product
```

### GROUP BY (Grouping Data)

Group data and calculate statistics for each group:

```sql
-- Count users by age
SELECT age, COUNT(*) AS user_count
FROM users
GROUP BY age;

-- Result:
-- age | user_count
-- 25  | 3
-- 30  | 5
-- 35  | 2

-- Average price by category (if you had a category column)
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category;
```

### HAVING (Filtering Groups)

`WHERE` filters rows, `HAVING` filters groups:

```sql
-- Get ages that have more than 5 users
SELECT age, COUNT(*) AS user_count
FROM users
GROUP BY age
HAVING COUNT(*) > 5;
```

### Subqueries (Queries Inside Queries)

```sql
-- Find users older than the average age
SELECT name, age
FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- Find products more expensive than the average
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

### Indexes (Making Queries Faster)

Indexes are like a **table of contents** for your database:

```sql
-- Create an index on email (makes email searches super fast)
CREATE INDEX idx_users_email ON users(email);

-- Create an index on multiple columns
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);

-- See all indexes
\di
```

**When to use indexes:**
- Columns used in WHERE clauses frequently
- Foreign keys (usually auto-indexed)
- Columns used for sorting (ORDER BY)

**Trade-off:** Indexes make reads faster but writes slightly slower.

### Transactions (All or Nothing)

Transactions ensure **multiple operations** either all succeed or all fail:

```sql
-- Start a transaction
BEGIN;

-- Transfer money from account A to account B
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If everything is good, commit (save)
COMMIT;

-- If something went wrong, rollback (undo)
ROLLBACK;
```

**Real-world example:**
```sql
BEGIN;

-- Create order
INSERT INTO orders (user_id, total_amount) VALUES (1, 150.00);

-- Add items
INSERT INTO order_items (order_id, product_id, quantity, price) 
VALUES (1, 5, 2, 75.00);

-- Update product stock
UPDATE products SET stock = stock - 2 WHERE id = 5;

-- If stock goes negative, rollback
-- Otherwise, commit
COMMIT;
```

---

## Connecting PostgreSQL with Python

### Installation

First, install the PostgreSQL driver for Python:

```bash
pip install psycopg2-binary
# or for async
pip install asyncpg
```

### Method 1: Using psycopg2 (Synchronous)

```python
import psycopg2
from psycopg2 import sql

# Step 1: Connect to database
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="my_first_db",
    user="postgres",
    password="your_password_here"
)

# Step 2: Create a cursor (the worker that executes commands)
cursor = connection.cursor()

# Step 3: Execute SQL
cursor.execute("SELECT * FROM users")

# Step 4: Fetch results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Step 5: Close connection
cursor.close()
connection.close()
```

**Complete Example: Creating and Querying**

```python
import psycopg2

# Connect
conn = psycopg2.connect(
    host="localhost",
    database="my_first_db",
    user="postgres",
    password="your_password"
)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
""")

# Insert data (using parameterized queries - SAFE!)
cursor.execute(
    "INSERT INTO products (name, price) VALUES (%s, %s)",
    ("Laptop", 999.99)
)

# Insert multiple
products = [
    ("Mouse", 29.99),
    ("Keyboard", 79.99),
    ("Monitor", 299.99)
]
cursor.executemany(
    "INSERT INTO products (name, price) VALUES (%s, %s)",
    products
)

# Commit changes
conn.commit()

# Query data
cursor.execute("SELECT * FROM products WHERE price > %s", (50,))
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Price: ${row[2]}")

# Clean up
cursor.close()
conn.close()
```

**⚠️ CRITICAL: Always use parameterized queries!**

```python
# ✅ GOOD - Safe from SQL injection
cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))

# ❌ BAD - Vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

### Method 2: Using asyncpg (Asynchronous)

For modern async Python applications:

```python
import asyncio
import asyncpg

async def main():
    # Connect
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        database="my_first_db",
        user="postgres",
        password="your_password"
    )
    
    # Execute query
    rows = await conn.fetch("SELECT * FROM users")
    for row in rows:
        print(row['name'], row['email'])
    
    # Insert data
    await conn.execute(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        "Alice", "alice@email.com"
    )
    
    # Close connection
    await conn.close()

# Run the async function
asyncio.run(main())
```

**Note:** `asyncpg` uses `$1, $2, $3` instead of `%s` for parameters.

### Method 3: Using SQLAlchemy (ORM)

SQLAlchemy lets you work with databases using Python classes instead of SQL:

```python
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Session

# Step 1: Create base class
class Base(DeclarativeBase):
    pass

# Step 2: Define your table as a Python class
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

# Step 3: Create engine (connection)
engine = create_engine(
    "postgresql://postgres:password@localhost/my_first_db"
)

# Step 4: Create tables
Base.metadata.create_all(engine)

# Step 5: Use the database
with Session(engine) as session:
    # Create a product (Python object)
    new_product = Product(name="Laptop", price=999.99)
    
    # Add to session
    session.add(new_product)
    
    # Save to database
    session.commit()
    
    # Query products
    products = session.query(Product).filter(Product.price > 500).all()
    for product in products:
        print(f"{product.name}: ${product.price}")
```

### Connection String Format

```python
# Standard format
"postgresql://username:password@host:port/database"

# Examples
"postgresql://postgres:mypass@localhost:5432/mydb"
"postgresql://user:pass@192.168.1.100:5432/production_db"
"postgresql://user:pass@db.example.com:5432/mydb"
```

---

## SQLAlchemy: The Python Way to Work with PostgreSQL

### What is SQLAlchemy?

**Simple Explanation:**
SQLAlchemy is like a **translator** between Python and PostgreSQL. Instead of writing SQL directly, you write Python code, and SQLAlchemy converts it to SQL for you.

**Why Use SQLAlchemy?**
- ✅ **Write Python, not SQL** - Use Python classes and objects
- ✅ **Type Safety** - Your IDE knows what columns exist
- ✅ **Automatic Relationships** - Access related data easily
- ✅ **Database Portability** - Switch from PostgreSQL to MySQL easily
- ✅ **Less Boilerplate** - No manual SQL string building
- ✅ **Security** - Automatically prevents SQL injection

**Real-World Analogy:**
- **Raw SQL** = Writing in assembly language (very detailed, error-prone)
- **SQLAlchemy** = Writing in Python (high-level, easier, safer)

### SQLAlchemy Core vs ORM

SQLAlchemy has two ways to work:

1. **SQLAlchemy Core** - Lower level, more control, closer to raw SQL
2. **SQLAlchemy ORM** - Higher level, Python classes, easier to use

**We'll focus on ORM** (the easier, more common way).

### Installation

```bash
pip install sqlalchemy
pip install psycopg2-binary  # PostgreSQL driver
# or for async
pip install asyncpg
```

---

## SQLAlchemy Fundamentals: Building Blocks

### Step 1: Create the Base Class

**What it is:** The foundation that all your table models inherit from.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

**Why:** This gives all your models the power to create tables, relationships, and more.

### Step 2: Create the Engine

**What it is:** The connection to your PostgreSQL database.

```python
from sqlalchemy import create_engine

# Synchronous engine
engine = create_engine(
    "postgresql://postgres:password@localhost:5432/mydb",
    echo=True  # Shows SQL queries in console (great for learning!)
)
```

**Breaking it down:**
- `postgresql://` = Protocol
- `postgres:password` = Username and password
- `localhost:5432` = Host and port
- `mydb` = Database name
- `echo=True` = Print all SQL queries (helpful for debugging)

**Async Engine (for modern async Python):**
```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://postgres:password@localhost:5432/mydb",
    echo=True
)
```

### Step 3: Define Your First Model

**What is a Model?** A Python class that represents a database table.

```python
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base  # Your Base class

class User(Base):
    __tablename__ = "users"  # The actual table name in PostgreSQL
    
    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
```

**Breaking down each line:**

1. **`class User(Base):`**
   - Inherits from `Base` (gives it database powers)
   - `User` is a Python class representing the `users` table

2. **`__tablename__ = "users"`**
   - Tells SQLAlchemy: "This class represents the 'users' table"
   - The table name in PostgreSQL will be `users`

3. **`id: Mapped[int] = mapped_column(primary_key=True)`**
   - `Mapped[int]` = Type hint: "This is an integer"
   - `mapped_column()` = Creates a database column
   - `primary_key=True` = This is the unique identifier

4. **`name: Mapped[str] = mapped_column(String(100), nullable=False)`**
   - `Mapped[str]` = Type hint: "This is a string"
   - `String(100)` = VARCHAR(100) in PostgreSQL
   - `nullable=False` = This field is required (NOT NULL)

5. **`email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)`**
   - `unique=True` = No two users can have the same email
   - `nullable=False` = Required field

6. **`age: Mapped[int | None] = mapped_column(Integer, nullable=True)`**
   - `int | None` = Can be an integer OR None (optional)
   - `nullable=True` = This field is optional

### Step 4: Create Tables in Database

```python
# Create all tables defined in models that inherit from Base
Base.metadata.create_all(engine)
```

**What this does:**
- Looks at all classes that inherit from `Base`
- Creates the corresponding tables in PostgreSQL
- If tables already exist, it does nothing (safe to run multiple times)

**Complete Example:**
```python
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Base class
class Base(DeclarativeBase):
    pass

# 2. Model
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)

# 3. Engine
engine = create_engine("postgresql://postgres:pass@localhost/mydb")

# 4. Create tables
Base.metadata.create_all(engine)
print("✅ Tables created!")
```

---

## SQLAlchemy Data Types

### Common Column Types

```python
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, DECIMAL
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    
    # Text types
    name: Mapped[str] = mapped_column(String(100))  # VARCHAR(100)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)  # Unlimited text
    
    # Number types
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # INTEGER
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))  # For money (precise)
    rating: Mapped[float] = mapped_column(Float)  # Floating point
    
    # Boolean
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Date/Time
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

### Column Options

```python
class User(Base):
    __tablename__ = "users"
    
    # Primary key (auto-incrementing)
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Unique constraint
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    # Not null (required)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Default value
    age: Mapped[int] = mapped_column(Integer, default=0)
    
    # Index (makes queries faster)
    email: Mapped[str] = mapped_column(String(255), index=True)
    
    # Multiple options combined
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
```

---

## Working with Data in SQLAlchemy

### Creating a Session

**What is a Session?** A session is like a "workspace" where you do database operations.

```python
from sqlalchemy.orm import Session

# Create a session
with Session(engine) as session:
    # Do database operations here
    pass
# Session automatically closes when done
```

### CREATE: Inserting Data

#### Insert One Row

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    # Create a Python object (not in database yet!)
    new_user = User(name="Alice", email="alice@email.com", age=25)
    
    # Add to session
    session.add(new_user)
    
    # Save to database (commit the transaction)
    session.commit()
    
    # After commit, new_user.id is automatically set!
    print(f"Created user with ID: {new_user.id}")
```

**Step-by-step:**
1. `User(...)` = Create Python object in memory
2. `session.add()` = "Hey session, track this object"
3. `session.commit()` = "Save everything to database"
4. After commit, `new_user.id` is automatically filled in by PostgreSQL

#### Insert Multiple Rows

```python
with Session(engine) as session:
    # Create multiple objects
    users = [
        User(name="Bob", email="bob@email.com", age=30),
        User(name="Charlie", email="charlie@email.com", age=28),
        User(name="David", email="david@email.com", age=22)
    ]
    
    # Add all at once
    session.add_all(users)
    
    # Commit once (more efficient!)
    session.commit()
    
    # All users now have IDs
    for user in users:
        print(f"{user.name}: ID {user.id}")
```

### READ: Querying Data

#### Get All Rows

```python
from sqlalchemy import select

with Session(engine) as session:
    # Modern way (SQLAlchemy 2.0+)
    stmt = select(User)
    users = session.scalars(stmt).all()
    
    for user in users:
        print(f"{user.name} - {user.email}")
```

#### Get One Row by ID

```python
with Session(engine) as session:
    # Get user with ID 1
    user = session.get(User, 1)  # Returns None if not found
    
    if user:
        print(f"Found: {user.name}")
    else:
        print("User not found")
```

#### Filter with WHERE

```python
from sqlalchemy import select

with Session(engine) as session:
    # Get users older than 25
    stmt = select(User).where(User.age > 25)
    users = session.scalars(stmt).all()
    
    # Get user by email
    stmt = select(User).where(User.email == "alice@email.com")
    user = session.scalar(stmt)  # Returns one result or None
    
    # Multiple conditions
    stmt = select(User).where(
        (User.age > 25) & (User.email.like("%@email.com"))
    )
    users = session.scalars(stmt).all()
```

**Filter Operators:**
```python
# Comparison
User.age > 25
User.age < 30
User.age >= 18
User.age <= 65
User.age == 25
User.age != 25

# Text matching
User.email.like("%@gmail.com")  # Ends with @gmail.com
User.name.contains("Alice")  # Contains "Alice"
User.email.in_(["alice@email.com", "bob@email.com"])  # In list

# Null checks
User.age.is_(None)  # Is NULL
User.age.is_not(None)  # Is NOT NULL

# Combining conditions
(User.age > 25) & (User.email.like("%@email.com"))  # AND
(User.age < 18) | (User.age > 65)  # OR
~(User.age == 25)  # NOT
```

#### Sorting (ORDER BY)

```python
from sqlalchemy import select

with Session(engine) as session:
    # Sort by age (ascending)
    stmt = select(User).order_by(User.age)
    users = session.scalars(stmt).all()
    
    # Sort by age (descending)
    stmt = select(User).order_by(User.age.desc())
    users = session.scalars(stmt).all()
    
    # Sort by multiple columns
    stmt = select(User).order_by(User.age.desc(), User.name)
    users = session.scalars(stmt).all()
```

#### Limiting Results

```python
with Session(engine) as session:
    # Get first 5 users
    stmt = select(User).limit(5)
    users = session.scalars(stmt).all()
    
    # Pagination: skip first 10, get next 5
    stmt = select(User).offset(10).limit(5)
    users = session.scalars(stmt).all()
```

#### Counting

```python
from sqlalchemy import func, select

with Session(engine) as session:
    # Count all users
    stmt = select(func.count(User.id))
    count = session.scalar(stmt)
    print(f"Total users: {count}")
    
    # Count with condition
    stmt = select(func.count(User.id)).where(User.age > 25)
    count = session.scalar(stmt)
    print(f"Users over 25: {count}")
```

### UPDATE: Modifying Data

```python
with Session(engine) as session:
    # Get the user
    user = session.get(User, 1)
    
    if user:
        # Modify the object
        user.age = 26
        user.name = "Alice Updated"
        
        # Commit to save changes
        session.commit()
        print("User updated!")
```

**Or update multiple rows:**
```python
from sqlalchemy import update

with Session(engine) as session:
    # Update all users under 18 to age 18
    stmt = update(User).where(User.age < 18).values(age=18)
    session.execute(stmt)
    session.commit()
    print("Updated all users under 18")
```

### DELETE: Removing Data

```python
with Session(engine) as session:
    # Get the user
    user = session.get(User, 1)
    
    if user:
        # Delete it
        session.delete(user)
        session.commit()
        print("User deleted!")
```

**Or delete multiple rows:**
```python
from sqlalchemy import delete

with Session(engine) as session:
    # Delete all users under 18
    stmt = delete(User).where(User.age < 18)
    session.execute(stmt)
    session.commit()
    print("Deleted all users under 18")
```

---

## Relationships in SQLAlchemy

### Understanding Relationships

**Real-World Analogy:**
- A **User** can write many **Posts**
- Each **Post** belongs to one **User**
- This is a **one-to-many** relationship

### One-to-Many Relationship

**Example: Users and Posts**

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Parent table (one user has many posts)
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # THE MAGIC: Relationship
    # This creates a list of Post objects
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

# Child table (many posts belong to one user)
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    
    # Foreign Key: The actual database column
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # THE MAGIC: Relationship
    # This creates a link to the User object
    user: Mapped["User"] = relationship(back_populates="posts")
```

**Breaking it down:**

1. **`user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))`**
   - Creates a column `user_id` in the `posts` table
   - References `id` in the `users` table
   - This is the **actual database column**

2. **`user: Mapped["User"] = relationship(back_populates="posts")`**
   - Creates a Python-side link
   - `post.user` gives you the User object
   - `back_populates="posts"` links to `User.posts`

3. **`posts: Mapped[list["Post"]] = relationship(back_populates="user")`**
   - Creates a Python-side link
   - `user.posts` gives you a list of Post objects
   - `back_populates="user"` links to `Post.user`

**Using the relationship:**

```python
with Session(engine) as session:
    # Create a user
    user = User(name="Alice")
    session.add(user)
    session.commit()
    
    # Create posts for this user
    post1 = Post(title="My First Post", content="Hello!", user_id=user.id)
    post2 = Post(title="My Second Post", content="World!", user_id=user.id)
    
    session.add_all([post1, post2])
    session.commit()
    
    # THE MAGIC: Access posts through relationship
    print(f"{user.name} has {len(user.posts)} posts")
    for post in user.posts:
        print(f"  - {post.title}")
    
    # THE MAGIC: Access user through relationship
    print(f"Post '{post1.title}' was written by {post1.user.name}")
```

**Even better: Create posts through the relationship:**

```python
with Session(engine) as session:
    # Create user
    user = User(name="Bob")
    session.add(user)
    session.flush()  # Get user.id without committing
    
    # Create posts through relationship (no need to set user_id manually!)
    post1 = Post(title="Post 1", content="Content 1")
    post2 = Post(title="Post 2", content="Content 2")
    
    # Add posts to user's posts list
    user.posts.append(post1)
    user.posts.append(post2)
    
    # SQLAlchemy automatically sets user_id!
    session.commit()
    
    print(f"User {user.name} has {len(user.posts)} posts")
```

### Many-to-Many Relationship

**Example: Posts and Tags** (a post can have many tags, a tag can be on many posts)

```python
from sqlalchemy import Table, Column, Integer, ForeignKey

# Junction table (the "middle" table)
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    
    # Many-to-many relationship
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    # Many-to-many relationship
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )
```

**Using many-to-many:**

```python
with Session(engine) as session:
    # Create post
    post = Post(title="Python Tutorial")
    
    # Create tags
    tag1 = Tag(name="python")
    tag2 = Tag(name="tutorial")
    
    # Link them (SQLAlchemy handles the junction table!)
    post.tags.append(tag1)
    post.tags.append(tag2)
    
    session.add(post)
    session.commit()
    
    # Access tags through relationship
    print(f"Post '{post.title}' has tags: {[tag.name for tag in post.tags]}")
```

### Relationship Options

```python
# Cascade delete (if user is deleted, delete their posts)
posts: Mapped[list["Post"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"  # Delete posts when user is deleted
)

# Lazy loading (default - loads when accessed)
posts: Mapped[list["Post"]] = relationship(back_populates="user", lazy="select")

# Eager loading (loads immediately with JOIN)
posts: Mapped[list["Post"]] = relationship(back_populates="user", lazy="joined")

# Lazy="dynamic" (returns a query object you can filter)
posts: Mapped[list["Post"]] = relationship(back_populates="user", lazy="dynamic")
```

---

## Advanced SQLAlchemy Queries

### JOINs

**Automatic JOINs through relationships:**
```python
# Get user with all their posts (automatic JOIN)
user = session.get(User, 1)
posts = user.posts  # SQLAlchemy automatically does a JOIN

# Manual JOIN
from sqlalchemy import select

stmt = select(User, Post).join(Post).where(User.id == 1)
results = session.execute(stmt).all()
```

### Aggregations

```python
from sqlalchemy import func, select

# Count posts per user
stmt = (
    select(User.name, func.count(Post.id).label("post_count"))
    .join(Post)
    .group_by(User.id, User.name)
)
results = session.execute(stmt).all()

for user_name, post_count in results:
    print(f"{user_name}: {post_count} posts")
```

### Subqueries

```python
from sqlalchemy import select

# Find users who have more than 5 posts
subquery = (
    select(Post.user_id, func.count(Post.id).label("count"))
    .group_by(Post.user_id)
    .having(func.count(Post.id) > 5)
    .subquery()
)

stmt = select(User).join(subquery, User.id == subquery.c.user_id)
users = session.scalars(stmt).all()
```

---

## Async SQLAlchemy

**Why Async?** For modern async Python applications (FastAPI, etc.)

### Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Async engine
engine = create_async_engine(
    "postgresql+asyncpg://postgres:password@localhost/mydb",
    echo=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Using Async Sessions

```python
async def create_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        user = User(name=name, email=email)
        session.add(user)
        await session.commit()  # Note: await!
        await session.refresh(user)  # Get the ID
        return user

async def get_users():
    async with AsyncSessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)  # Note: await!
        users = result.scalars().all()
        return users
```

**Key differences:**
- Use `asyncpg` driver: `postgresql+asyncpg://...`
- Use `AsyncSession` instead of `Session`
- Use `await` for all database operations
- Use `await session.execute()` instead of `session.scalars()`

---

## Database Migrations with Alembic

**What are Migrations?** A way to track and apply changes to your database schema over time.

### Setup Alembic

```bash
pip install alembic
```

```bash
# Initialize Alembic in your project
alembic init alembic
```

### Configure Alembic

Edit `alembic/env.py`:
```python
from database import Base
from models import User, Post  # Import all your models

# Set the target metadata
target_metadata = Base.metadata
```

Edit `alembic.ini`:
```ini
sqlalchemy.url = postgresql://postgres:password@localhost/mydb
```

### Creating Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Create users and posts tables"

# This creates a file in alembic/versions/ with your changes
```

### Applying Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# See migration history
alembic history
```

**Why use migrations?**
- ✅ Track all database changes
- ✅ Apply changes consistently across environments
- ✅ Rollback if something goes wrong
- ✅ Team collaboration (everyone has same schema)

---

## SQLAlchemy Best Practices

### 1. Always Use Sessions as Context Managers

```python
# ✅ GOOD
with Session(engine) as session:
    user = User(name="Alice")
    session.add(user)
    session.commit()

# ❌ BAD
session = Session(engine)
user = User(name="Alice")
session.add(user)
session.commit()
session.close()  # Easy to forget!
```

### 2. Use Type Hints

```python
# ✅ GOOD
id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column(String(100))

# ❌ BAD (old style)
id = Column(Integer, primary_key=True)
```

### 3. Always Commit or Rollback

```python
try:
    with Session(engine) as session:
        user = User(name="Alice")
        session.add(user)
        session.commit()
except Exception as e:
    session.rollback()  # Undo changes on error
    raise e
```

### 4. Use Relationships Instead of Manual JOINs

```python
# ✅ GOOD
user = session.get(User, 1)
posts = user.posts  # Automatic JOIN

# ❌ Less ideal
stmt = select(Post).join(User).where(User.id == 1)
```

### 5. Enable Echo for Development

```python
engine = create_engine(..., echo=True)  # See all SQL queries
```

### 6. Use Connection Pooling

```python
engine = create_engine(
    "postgresql://...",
    pool_size=10,  # Max connections
    max_overflow=20  # Extra connections if needed
)
```

---

## Real-World SQLAlchemy Examples

### Example 1: Blog System with SQLAlchemy

```python
from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship()
```

**Using it:**
```python
with Session(engine) as session:
    # Create user
    user = User(username="alice", email="alice@email.com")
    session.add(user)
    session.flush()
    
    # Create post
    post = Post(
        title="My First Post",
        content="This is my first blog post!",
        author_id=user.id
    )
    session.add(post)
    session.flush()
    
    # Create comment
    comment = Comment(
        content="Great post!",
        post_id=post.id,
        author_id=user.id
    )
    session.add(comment)
    session.commit()
    
    # Access through relationships
    print(f"{user.username} wrote {len(user.posts)} posts")
    print(f"Post '{post.title}' has {len(post.comments)} comments")
```

### Example 2: FastAPI with SQLAlchemy

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

# Dependency to get database session
def get_db():
    with Session(engine) as session:
        yield session

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email}

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    return {"id": user.id, "name": user.name, "email": user.email, "posts": len(user.posts)}
```

---

## SQLAlchemy vs Raw SQL: When to Use What?

### Use SQLAlchemy When:
- ✅ Building applications (web apps, APIs)
- ✅ Need relationships and complex queries
- ✅ Want type safety and IDE support
- ✅ Working in a team (consistent code style)
- ✅ Need database portability

### Use Raw SQL When:
- ✅ Simple scripts or one-off tasks
- ✅ Performance-critical operations
- ✅ Complex queries that are hard in ORM
- ✅ Learning SQL fundamentals
- ✅ Database-specific features

**Most projects use SQLAlchemy for the main code and raw SQL for specific optimizations.**

---

## Summary: SQLAlchemy Building Blocks

You've learned:

✅ **What SQLAlchemy is** - Python ORM for databases  
✅ **Setting up** - Base class, Engine, Models  
✅ **Data types** - String, Integer, DateTime, etc.  
✅ **CRUD operations** - Create, Read, Update, Delete  
✅ **Relationships** - One-to-many, Many-to-many  
✅ **Advanced queries** - JOINs, aggregations, subqueries  
✅ **Async SQLAlchemy** - For modern async applications  
✅ **Migrations** - Alembic for schema changes  
✅ **Best practices** - How to write good SQLAlchemy code  

**You can now build production-ready applications with SQLAlchemy and PostgreSQL!** 🚀

---

## Real-World Examples

### Example 1: User Authentication System

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Sessions table (track who's logged in)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
```

**Python code to authenticate:**
```python
import psycopg2
import hashlib
from datetime import datetime, timedelta

def authenticate_user(username: str, password: str):
    conn = psycopg2.connect(
        host="localhost",
        database="myapp",
        user="postgres",
        password="password"
    )
    cursor = conn.cursor()
    
    # Find user
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    
    if not user:
        return None  # User not found
    
    user_id, stored_hash = user
    
    # Check password (in real app, use bcrypt, not simple hash!)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if password_hash == stored_hash:
        # Create session
        expires_at = datetime.now() + timedelta(days=7)
        cursor.execute(
            "INSERT INTO sessions (user_id, expires_at) VALUES (%s, %s)",
            (user_id, expires_at)
        )
        conn.commit()
        return user_id
    
    return None  # Wrong password
```

### Example 2: Blog System with Comments

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Posts
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments (comments on posts)
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags (many-to-many with posts)
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Post tags (junction table)
CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

**Query to get a post with all its comments and tags:**
```sql
SELECT 
    p.id,
    p.title,
    p.content,
    u.username AS author,
    array_agg(DISTINCT t.name) AS tags,
    json_agg(
        json_build_object(
            'id', c.id,
            'content', c.content,
            'author', u2.username,
            'created_at', c.created_at
        )
    ) AS comments
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN post_tags pt ON p.id = pt.post_id
LEFT JOIN tags t ON pt.tag_id = t.id
LEFT JOIN comments c ON p.id = c.post_id
LEFT JOIN users u2 ON c.author_id = u2.id
WHERE p.id = 1
GROUP BY p.id, p.title, p.content, u.username;
```

### Example 3: E-Commerce Shopping Cart

```sql
-- Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category_id INTEGER REFERENCES categories(id)
);

-- Categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    address TEXT
);

-- Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

**Python function to create an order:**
```python
def create_order(customer_id: int, items: list):
    """
    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
    """
    conn = psycopg2.connect(...)
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Calculate total
        total = 0
        for item in items:
            cursor.execute(
                "SELECT price, stock FROM products WHERE id = %s",
                (item["product_id"],)
            )
            product = cursor.fetchone()
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
            
            price, stock = product
            if stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for product {item['product_id']}")
            
            total += price * item["quantity"]
        
        # Create order
        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s) RETURNING id",
            (customer_id, total)
        )
        order_id = cursor.fetchone()[0]
        
        # Add order items and update stock
        for item in items:
            cursor.execute(
                "SELECT price FROM products WHERE id = %s",
                (item["product_id"],)
            )
            price = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item["product_id"], item["quantity"], price)
            )
            
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item["quantity"], item["product_id"])
            )
        
        # Commit transaction
        conn.commit()
        return order_id
        
    except Exception as e:
        # Rollback on error
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
```

---

## Best Practices and Security

### 1. Always Use Parameterized Queries

```python
# ✅ GOOD
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# ❌ BAD - SQL Injection vulnerability
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**Why?** If someone enters `email = "'; DROP TABLE users; --"`, the bad code would delete your entire users table!

### 2. Use Connection Pooling

For web applications, reuse connections instead of creating new ones:

```python
from psycopg2 import pool

# Create connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="localhost",
    database="mydb",
    user="postgres",
    password="password"
)

# Get connection from pool
conn = connection_pool.getconn()

# Use connection
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
# ... do work ...

# Return connection to pool
connection_pool.putconn(conn)
```

### 3. Always Close Connections

```python
# ✅ GOOD - Use context manager
with psycopg2.connect(...) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        # Auto-closes when done

# ✅ ALSO GOOD - Manual cleanup
conn = psycopg2.connect(...)
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
finally:
    cursor.close()
    conn.close()
```

### 4. Use Transactions for Multiple Operations

```python
conn = psycopg2.connect(...)
try:
    cursor = conn.cursor()
    cursor.execute("BEGIN")
    
    # Multiple operations
    cursor.execute("INSERT INTO orders ...")
    cursor.execute("UPDATE products SET stock = stock - 1 ...")
    
    conn.commit()  # Save all changes
except Exception as e:
    conn.rollback()  # Undo all changes on error
    raise e
```

### 5. Create Indexes on Frequently Queried Columns

```sql
-- Index on email (used in WHERE clauses)
CREATE INDEX idx_users_email ON users(email);

-- Index on foreign keys
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index (multiple columns)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, created_at);
```

### 6. Use Appropriate Data Types

```sql
-- ✅ GOOD
price DECIMAL(10, 2)  -- For money
age INTEGER           -- For whole numbers
created_at TIMESTAMP  -- For dates/times

-- ❌ BAD
price VARCHAR(50)     -- Don't store numbers as text!
age TEXT              -- Use INTEGER instead
```

### 7. Set Up Proper Permissions

```sql
-- Create a user for your application (not the superuser!)
CREATE USER myapp_user WITH PASSWORD 'secure_password';

-- Grant only necessary permissions
GRANT CONNECT ON DATABASE mydb TO myapp_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO myapp_user;
```

### 8. Regular Backups

```bash
# Backup database
pg_dump -U postgres mydb > backup.sql

# Restore database
psql -U postgres mydb < backup.sql
```

### 9. Use Environment Variables for Credentials

```python
import os
import psycopg2

# ✅ GOOD - From environment
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# ❌ BAD - Hardcoded
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="mypassword123"  # Never do this!
)
```

---

## Troubleshooting Common Issues

### Issue 1: "Connection Refused"

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check if PostgreSQL is running:
   ```bash
   # Windows
   # Check Services app
   
   # Mac/Linux
   sudo systemctl status postgresql
   ```

2. Check the port (default is 5432):
   ```python
   # Try connecting with explicit port
   conn = psycopg2.connect(..., port=5432)
   ```

3. Check firewall settings

### Issue 2: "Authentication Failed"

**Error:** `psycopg2.OperationalError: password authentication failed`

**Solutions:**
1. Verify username and password
2. Check `pg_hba.conf` file (PostgreSQL authentication config)
3. Reset password:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

### Issue 3: "Database Does Not Exist"

**Error:** `psycopg2.OperationalError: database "mydb" does not exist`

**Solution:**
```sql
-- Create the database
CREATE DATABASE mydb;
```

### Issue 4: "Relation Does Not Exist"

**Error:** `psycopg2.ProgrammingError: relation "users" does not exist`

**Solutions:**
1. Check if you're connected to the right database:
   ```sql
   \c mydb  -- Connect to correct database
   ```

2. Check if table exists:
   ```sql
   \dt  -- List all tables
   ```

3. Create the table if it doesn't exist

### Issue 5: "Foreign Key Violation"

**Error:** `psycopg2.IntegrityError: insert or update on table "posts" violates foreign key constraint`

**Solution:**
- Make sure the referenced row exists first:
  ```sql
  -- ❌ This will fail if user_id 999 doesn't exist
  INSERT INTO posts (title, user_id) VALUES ('Test', 999);
  
  -- ✅ First create the user, then reference it
  INSERT INTO users (id, name) VALUES (999, 'Test User');
  INSERT INTO posts (title, user_id) VALUES ('Test', 999);
  ```

### Issue 6: "Unique Constraint Violation"

**Error:** `psycopg2.IntegrityError: duplicate key value violates unique constraint`

**Solution:**
- The value already exists. Either:
  - Use a different value
  - Update the existing row instead
  - Use `INSERT ... ON CONFLICT`:
    ```sql
    INSERT INTO users (email, name) 
    VALUES ('alice@email.com', 'Alice')
    ON CONFLICT (email) 
    DO UPDATE SET name = EXCLUDED.name;
    ```

### Issue 7: "Too Many Connections"

**Error:** Connection pool exhausted

**Solution:**
- Always close connections when done
- Use connection pooling
- Increase max connections in PostgreSQL config if needed

---

## Quick Reference Cheat Sheet

### Essential SQL Commands

```sql
-- Database operations
CREATE DATABASE mydb;
DROP DATABASE mydb;
\c mydb  -- Connect to database

-- Table operations
CREATE TABLE users (...);
DROP TABLE users;
ALTER TABLE users ADD COLUMN age INTEGER;
ALTER TABLE users DROP COLUMN age;
\d users  -- Describe table structure

-- Data operations
INSERT INTO users (name, email) VALUES ('Alice', 'alice@email.com');
SELECT * FROM users;
UPDATE users SET age = 25 WHERE id = 1;
DELETE FROM users WHERE id = 1;

-- Query operations
SELECT * FROM users WHERE age > 25;
SELECT * FROM users ORDER BY name ASC;
SELECT * FROM users LIMIT 10;
SELECT COUNT(*) FROM users;
SELECT age, COUNT(*) FROM users GROUP BY age;

-- Join operations
SELECT * FROM posts JOIN users ON posts.user_id = users.id;
```

### Python Connection Patterns

```python
# Synchronous (psycopg2)
import psycopg2
conn = psycopg2.connect(host="localhost", database="mydb", user="postgres", password="pass")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()

# Asynchronous (asyncpg)
import asyncpg
conn = await asyncpg.connect(host="localhost", database="mydb", user="postgres", password="pass")
rows = await conn.fetch("SELECT * FROM users")
await conn.close()

# SQLAlchemy ORM
from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:pass@localhost/mydb")
with Session(engine) as session:
    users = session.query(User).all()
```

---

## Next Steps

Now that you understand the fundamentals:

1. **Practice:** Create your own database and tables
2. **Build:** Create a small project (blog, todo app, etc.)
3. **Learn More:**
   - PostgreSQL full-text search
   - JSON/JSONB data types
   - Stored procedures and functions
   - Database migrations (Alembic)
   - Performance optimization
   - Replication and backups

4. **Resources:**
   - [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
   - [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
   - [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

## Summary

You've learned:

✅ **What PostgreSQL is** and why it's powerful  
✅ **How to install** PostgreSQL from scratch  
✅ **How to connect** to databases  
✅ **How to create tables** with proper data types  
✅ **CRUD operations** (Create, Read, Update, Delete)  
✅ **Relationships and Foreign Keys**  
✅ **JOINs** to combine data from multiple tables  
✅ **Advanced SQL** (aggregations, subqueries, transactions)  
✅ **How to connect** PostgreSQL with Python  
✅ **Real-world examples** (auth, blog, e-commerce)  
✅ **Best practices** and security  
✅ **Troubleshooting** common issues  

**You're now ready to build production-ready applications with PostgreSQL!** 🚀

Remember: The best way to learn is by doing. Start building something, make mistakes, fix them, and keep learning!

---

*This guide was created by a 20-year veteran backend developer to help beginners master PostgreSQL. Practice these concepts, experiment with your own projects, and don't be afraid to make mistakes - that's how you learn!*
