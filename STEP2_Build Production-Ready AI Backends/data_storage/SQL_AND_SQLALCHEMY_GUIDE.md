# SQL and SQLAlchemy Concepts Guide

This comprehensive guide explores raw SQL and SQLAlchemy concepts based on the examples in this codebase. It covers database fundamentals, table creation, relationships, and best practices.

---

## Table of Contents

1. [Introduction to Databases](#introduction-to-databases)
2. [Raw SQL Fundamentals](#raw-sql-fundamentals)
3. [SQLAlchemy Fundamentals](#sqlalchemy-fundamentals)
4. [Setting Up Tables in SQLAlchemy](#setting-up-tables-in-sqlalchemy)
5. [Raw SQL vs SQLAlchemy Comparison](#raw-sql-vs-sqlalchemy-comparison)
6. [Code Examples from This Codebase](#code-examples-from-this-codebase)
7. [Best Practices](#best-practices)

---

## Introduction to Databases

### What is a Database?

A database is an organized collection of data stored and accessed electronically. In this codebase, we use **SQLite**, a lightweight, file-based database that's perfect for development and small to medium applications.

### Key Concepts

- **Table**: A collection of related data organized in rows and columns
- **Row**: A single record in a table
- **Column**: A field that stores a specific type of data
- **Primary Key**: A unique identifier for each row
- **Foreign Key**: A reference to a primary key in another table (establishes relationships)
- **Relationship**: A connection between tables (one-to-many, many-to-one, etc.)

---

## Raw SQL Fundamentals

### Connection and Cursor Pattern

In raw SQL (using `sqlite3`), you work with two main objects:

1. **Connection**: The "road" to the database
2. **Cursor**: The "worker" that executes commands

```python
import sqlite3

# Create connection (creates database file if it doesn't exist)
connection = sqlite3.connect("database.db")

# Create cursor (the worker that executes commands)
cursor = connection.cursor()
```

### Creating Tables with Raw SQL

#### Basic Table Creation

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price DECIMAL
);
```

**Key SQL Keywords:**
- `CREATE TABLE`: Creates a new table
- `IF NOT EXISTS`: Prevents errors if table already exists
- `INTEGER PRIMARY KEY`: Auto-incrementing unique identifier
- `TEXT`: String data type
- `DECIMAL`: Floating-point number for prices
- `UNIQUE`: Ensures no duplicate values

#### Relational Tables (Foreign Keys)

```sql
-- Parent table (Brand)
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

-- Child table (Product) with foreign key
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price DECIMAL,
    brand_id INTEGER REFERENCES brands(id)
);
```

**Foreign Key Explanation:**
- `brand_id INTEGER REFERENCES brands(id)`: Creates a relationship
- `brand_id` stores the ID of a brand from the `brands` table
- This enforces referential integrity (can't delete a brand if products reference it)

### Inserting Data with Raw SQL

#### Simple Insert

```python
cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", 
               ("Laptop", 999.99))
connection.commit()  # Save changes!
```

**Important Notes:**
- Use `?` placeholders to prevent SQL injection
- Always pass values as tuples: `(value1, value2)`
- Call `connection.commit()` to save changes

#### Insert with Relationship

```python
# Step 1: Ensure brand exists (or create it)
cursor.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", 
               ("Nvidia",))

# Step 2: Get the brand ID
result = cursor.execute("SELECT id FROM brands WHERE name = ?", 
                        ("Nvidia",))
brand_id = result.fetchone()[0]  # Extract ID from tuple

# Step 3: Insert product with brand reference
cursor.execute("""
    INSERT INTO products (name, price, brand_id) 
    VALUES (?, ?, ?)
""", ("RTX 4090", 1600.00, brand_id))

connection.commit()
```

### Querying Data with Raw SQL

#### Basic SELECT

```python
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()  # Get all results
```

#### JOIN Query (Combining Tables)

```python
query = """
SELECT products.name, products.price, brands.name
FROM products
JOIN brands ON products.brand_id = brands.id
"""

cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(f"{row[0]} | ${row[1]} | {row[2]}")
```

**JOIN Explanation:**
- `JOIN` combines rows from two tables
- `ON products.brand_id = brands.id` specifies the relationship
- Result includes columns from both tables

#### Filtered Queries

```python
# Search with LIKE (pattern matching)
search_term = f"%RTX%"
cursor.execute("""
    SELECT * FROM products 
    WHERE name LIKE ?
""", (search_term,))
```

### Updating and Deleting

```python
# Update
cursor.execute("""
    UPDATE products 
    SET price = ? 
    WHERE name = ?
""", (1099.99, "Laptop"))
connection.commit()

# Delete
cursor.execute("DELETE FROM products WHERE name = ?", ("Laptop",))
connection.commit()
```

---

## SQLAlchemy Fundamentals

### What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and Object-Relational Mapping (ORM) library that provides:
- **Database abstraction**: Write Python code instead of raw SQL
- **Type safety**: Python type hints for database columns
- **Relationship management**: Easy handling of table relationships
- **Database portability**: Switch databases without changing code

### Core Components

1. **Engine**: Database connection pool
2. **Base**: Base class for all table models
3. **Session**: Interface for database operations
4. **Models**: Python classes representing database tables

---

## Setting Up Tables in SQLAlchemy

### Step 1: Import Required Modules

```python
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
```

### Step 2: Create Base Class

```python
class Base(DeclarativeBase):
    pass
```

The `Base` class is the foundation for all your table models. It provides the metadata and functionality needed for SQLAlchemy to work.

### Step 3: Define Your Table Model

#### Simple Table (No Relationships)

```python
class Product(Base):
    __tablename__ = "products"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # String column with uniqueness constraint
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # Float column
    price: Mapped[float] = mapped_column()
    
    def __repr__(self):
        return f"<Product {self.name}>"
```

**Key Components:**
- `__tablename__`: The actual table name in the database
- `Mapped[type]`: Type hint for the column (Python type)
- `mapped_column()`: SQLAlchemy column definition
- `primary_key=True`: Marks as primary key
- `String`: SQLAlchemy string type
- `unique=True`: Adds uniqueness constraint

#### Relational Tables (With Foreign Keys)

```python
# Parent Table
class Brand(Base):
    __tablename__ = "brands"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # Relationship: One brand has many products
    products: Mapped[list["Product"]] = relationship(back_populates="brand")
    
    def __repr__(self):
        return f"<Brand {self.name}>"

# Child Table
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column()
    
    # Foreign Key: The actual database column
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    
    # Relationship: Each product belongs to one brand
    brand: Mapped["Brand"] = relationship(back_populates="products")
    
    def __repr__(self):
        return f"<Product {self.name}>"
```

**Relationship Explanation:**
- `ForeignKey("brands.id")`: Creates the foreign key column in the database
- `relationship()`: Creates a Python-side link between objects
- `back_populates`: Links both sides of the relationship
- `Mapped[list["Product"]]`: One-to-many (one brand, many products)
- `Mapped["Brand"]`: Many-to-one (many products, one brand)

### Step 4: Create Engine and Tables

```python
# Create engine (connection to database)
engine = create_engine("sqlite:///database.db", echo=True)
# echo=True shows SQL queries in console (great for debugging!)

# Create all tables defined in Base subclasses
Base.metadata.create_all(engine)
```

**Engine URL Formats:**
- SQLite: `sqlite:///database.db` (file-based)
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`

### Complete Example: Setting Up a Table

```python
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Base class
class Base(DeclarativeBase):
    pass

# 2. Define model
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    price: Mapped[float] = mapped_column()
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    # nullable=True allows None values
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

# 3. Create engine and tables
engine = create_engine("sqlite:///my_store.db", echo=True)
Base.metadata.create_all(engine)

print("✅ Tables created successfully!")
```

### Advanced Column Types

```python
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text
from datetime import datetime

class AdvancedProduct(Base):
    __tablename__ = "advanced_products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Max length
    description: Mapped[str | None] = mapped_column(Text, nullable=True)  # Long text
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
```

### Common Column Options

```python
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Unique constraint
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # Not null (default behavior, but explicit)
    price: Mapped[float] = mapped_column(nullable=False)
    
    # Default value
    quantity: Mapped[int] = mapped_column(default=0)
    
    # Index for faster queries
    name: Mapped[str] = mapped_column(String, index=True)
    
    # Combination of options
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True
    )
```

---

## Raw SQL vs SQLAlchemy Comparison

### Creating Tables

#### Raw SQL
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        price DECIMAL
    )
""")
```

#### SQLAlchemy
```python
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    price: Mapped[float] = mapped_column()

Base.metadata.create_all(engine)
```

### Inserting Data

#### Raw SQL
```python
cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", 
               ("Laptop", 999.99))
connection.commit()
```

#### SQLAlchemy
```python
with Session(engine) as session:
    product = Product(name="Laptop", price=999.99)
    session.add(product)
    session.commit()
```

### Querying Data

#### Raw SQL
```python
cursor.execute("SELECT * FROM products WHERE price > ?", (500,))
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2])
```

#### SQLAlchemy
```python
from sqlalchemy import select

with Session(engine) as session:
    stmt = select(Product).where(Product.price > 500)
    products = session.scalars(stmt).all()
    for product in products:
        print(product.name, product.price)
```

### Joins

#### Raw SQL
```python
cursor.execute("""
    SELECT products.name, brands.name
    FROM products
    JOIN brands ON products.brand_id = brands.id
""")
```

#### SQLAlchemy
```python
with Session(engine) as session:
    products = session.scalars(select(Product)).all()
    for product in products:
        print(product.name, product.brand.name)  # Direct access!
```

---

## Code Examples from This Codebase

### Example 1: Library Database (test.py)

**Raw SQL approach** with authors and books relationship:

```python
# Creates two tables with foreign key relationship
worker.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
worker.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, author_id INTEGER REFERENCES authors(id))")

# Insert with relationship handling
worker.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author_name,))
result = worker.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
author_id = result.fetchone()[0]
worker.execute("INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)", 
               (title, year, author_id))
```

**Key Concepts Demonstrated:**
- Foreign key relationships
- `INSERT OR IGNORE` for safe inserts
- Fetching foreign key IDs
- JOIN queries for reading related data

### Example 2: Computer Store (shop_manager.py)

**Complete CRUD application** with raw SQL:

```python
# Table creation with foreign keys
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    price DECIMAL,
    brand_id INTEGER REFERENCES brands(id)
);

# Search with LIKE pattern matching
query = """
SELECT products.name, products.price, brands.name
FROM products
JOIN brands on products.brand_id = brands.id
WHERE products.name LIKE ?
"""
search_term = f"%{keyword}%"
worker.execute(query, (search_term,))
```

**Key Concepts Demonstrated:**
- Full CRUD operations (Create, Read, Update, Delete)
- Pattern matching with `LIKE`
- User input validation
- Error handling

### Example 3: SQLAlchemy Simple Table (orm_store.py)

**SQLAlchemy ORM** with safe inserts:

```python
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    price: Mapped[float] = mapped_column()

# Safe insert with conflict handling
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

stmt = sqlite_insert(Product).values(name=item["name"], price=item["price"])
stmt = stmt.on_conflict_do_nothing(index_elements=['name'])
session.execute(stmt)
```

**Key Concepts Demonstrated:**
- SQLAlchemy model definition
- Session management
- Safe inserts with conflict handling
- Using `select()` for queries

### Example 4: SQLAlchemy Relationships (orm_relational.py)

**SQLAlchemy ORM** with bidirectional relationships:

```python
class Brand(Base):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="brand")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column()
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    brand: Mapped["Brand"] = relationship(back_populates="products")
```

**Key Concepts Demonstrated:**
- Foreign keys in SQLAlchemy
- Bidirectional relationships
- `back_populates` for relationship linking
- Type hints with `Mapped[]`

---

## Best Practices

### Raw SQL Best Practices

1. **Always use parameterized queries** (prevent SQL injection):
   ```python
   # ✅ Good
   cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
   
   # ❌ Bad (SQL injection risk)
   cursor.execute(f"SELECT * FROM products WHERE name = '{name}'")
   ```

2. **Always commit transactions**:
   ```python
   cursor.execute("INSERT INTO products ...")
   connection.commit()  # Don't forget!
   ```

3. **Use context managers** for automatic cleanup:
   ```python
   with sqlite3.connect("db.db") as conn:
       cursor = conn.cursor()
       # ... operations ...
       conn.commit()  # Auto-commits on success
   ```

4. **Handle errors appropriately**:
   ```python
   try:
       cursor.execute("INSERT INTO products ...")
       connection.commit()
   except sqlite3.IntegrityError:
       print("Duplicate entry!")
   except Exception as e:
       print(f"Error: {e}")
   ```

### SQLAlchemy Best Practices

1. **Use sessions as context managers**:
   ```python
   with Session(engine) as session:
       product = Product(name="Laptop", price=999.99)
       session.add(product)
       session.commit()
   ```

2. **Use type hints** for better IDE support:
   ```python
   id: Mapped[int] = mapped_column(primary_key=True)
   ```

3. **Define `__repr__` methods** for debugging:
   ```python
   def __repr__(self):
       return f"<Product {self.name}>"
   ```

4. **Use relationships instead of manual joins**:
   ```python
   # ✅ Good
   product.brand.name
   
   # ❌ Less ideal
   session.query(Product).join(Brand).filter(...)
   ```

5. **Enable echo for development**:
   ```python
   engine = create_engine("sqlite:///db.db", echo=True)
   # Shows all SQL queries in console
   ```

### General Database Best Practices

1. **Use transactions** for multiple related operations
2. **Index frequently queried columns** for performance
3. **Use appropriate data types** (don't store numbers as text)
4. **Normalize your database** (avoid data duplication)
5. **Back up your database** regularly
6. **Use migrations** for production (Alembic with SQLAlchemy)

---

## Summary

### When to Use Raw SQL

- Simple, straightforward queries
- Performance-critical operations
- Learning SQL fundamentals
- Small projects or scripts
- When you need direct control over SQL

### When to Use SQLAlchemy

- Complex applications with many relationships
- Need database portability
- Want type safety and IDE support
- Building maintainable, scalable applications
- Team projects where consistency matters

### Key Takeaways

1. **Raw SQL** gives you direct control and is great for learning
2. **SQLAlchemy** provides abstraction and makes complex relationships easier
3. **Both approaches** are valid - choose based on your needs
4. **Relationships** are fundamental to relational databases
5. **Always use parameterized queries** to prevent SQL injection
6. **Transactions** ensure data consistency

---

## Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Database Design Fundamentals](https://en.wikipedia.org/wiki/Database_design)

---

*This guide was generated based on the code examples in the `data_storage` folder. For hands-on practice, run the example files and experiment with the concepts demonstrated.*
