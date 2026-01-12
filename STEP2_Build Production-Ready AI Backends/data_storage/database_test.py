import sqlite3

# 1. Connect to the database
# If the file doesn't exist, Python creates it automatically.
connection = sqlite3.connect("hardware_store_python.db")

# 2. Create the "Cursor" (The Robot Arm)
cursor = connection.cursor()

# 3. Define our SQL commands (exactly what we wrote before)
# We use triple quotes (""") so we can write multi-line SQL.
setup_sql = """
-- CLEANUP: Start fresh every time
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS brands;

-- STRUCTURE: Create the tables
CREATE TABLE brands (
    id INTEGER PRIMARY KEY, 
    name TEXT UNIQUE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    price DECIMAL, 
    brand_id INTEGER REFERENCES brands(id)
);

-- DATA: Insert the brands
INSERT INTO brands (id, name) VALUES (1, 'Nvidia');
INSERT INTO brands (id, name) VALUES (2, 'AMD');

-- DATA: Insert the products
INSERT INTO products (id, name, price, brand_id) 
VALUES (101, 'RTX 4090', 1600.00, 1);

INSERT INTO products (id, name, price, brand_id) 
VALUES (102, 'RX 7900 XTX', 999.00, 2);
"""

# 4. Run the setup
print("🔨 Building database...")
cursor.executescript(setup_sql) # executescript is great for running many commands at once

# 5. Save the changes! (Crucial step)
connection.commit()
print("✅ Database saved.")

# ---------------------------------------------------------

# 6. Now, let's READ the data back (The Report)
print("\n🔎 Running the JOIN query...")

query = """
SELECT products.name, products.price, brands.name
FROM products
JOIN brands ON products.brand_id = brands.id
"""

cursor.execute(query) # Run the query
rows = cursor.fetchall() # Grab all the results

# 7. Print the results nicely
print(f"{'PRODUCT':<15} | {'PRICE':<10} | {'BRAND':<10}")
print("-" * 40)
for row in rows:
    # row is a tuple: ('RTX 4090', 1600.0, 'Nvidia')
    print(f"{row[0]:<15} | ${row[1]:<9} | {row[2]}")

# 8. Close the connection
connection.close()