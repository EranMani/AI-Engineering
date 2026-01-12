import sqlite3

connection = sqlite3.connect("walmart.db")
worker = connection.cursor()

def build_database():
    create_table_command = """
    CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT UNIQUE);
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price DECIMAL, department_id INTEGER REFERENCES departments(id));
    """

    worker.executescript(create_table_command)
    print("Walmart database built.")

def stock_shelves():
    data = {
        "Electronics": {
            "Samsung TV": "500",
            "Sony Headphones": "100",
            "Generic Cable": "10"
        },
        "Groceries": {
            "Milk": "2",
            "Bread": "3",
            "Steak": "20"
        }
    }

    for d_name, d_items in data.items():
        worker.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (d_name, ))
        result = worker.execute("SELECT id FROM departments WHERE name = ?", (d_name, ))
        department_id = result.fetchone()[0]

        for name, price in d_items.items():
            worker.execute("INSERT INTO products (name, price, department_id) VALUES (?, ?, ?)", (name, price, department_id ))

    connection.commit()

def show_top_three():
    command = """
    SELECT products.name, products.price
    FROM products JOIN departments ON products.department_id = departments.id
    ORDER BY products.price DESC
    LIMIT 3;
    """

    result = worker.execute(command)
    all_rows = result.fetchall()

    if not all_rows:
        print("No items are currently on shelves!")
        return

    for row in all_rows:
        print(f"{row[0]} | {row[1]}")

def show_total_value():
    command = """
    SELECT SUM(price) FROM products
    """

    result = worker.execute(command)
    total_price = result.fetchone()[0]

    print(f"Total price of current items on shelves is: {total_price}")

build_database()
stock_shelves()
show_top_three()
show_total_value()
        
