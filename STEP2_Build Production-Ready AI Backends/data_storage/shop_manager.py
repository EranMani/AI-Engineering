from itertools import product
import sqlite3

# connect to the database
# if file doesnt exists, python will create it itself
connection = sqlite3.connect("computer_store.db")

# create the cursor
# cursor is the worker who actually does the tasks
# connection is the road, cursor is the truck driver
worker = connection.cursor()

print("successfully connected to the database!")

def setup_tables():
    sql_command = """
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
    """

    # tell the worker to run this command
    worker.executescript(sql_command)
    print("tables created successfully!")

def add_product(product_name, price, brand_name):
    try:
        # 1. First, we need to make sure the Brand exists.
        # We try to insert the brand. If it exists (IGNORE), we skip it.
        worker.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", (brand_name,))
        
        # 2. Get the ID of that brand so we can link the product
        # This is a mini-query to find the ID we just made (or found).
        result = worker.execute("SELECT id FROM brands WHERE name = ?", (brand_name,))
        brand_id = result.fetchone()[0] # Grab the first number from the result
        
        # 3. Add the product using that Brand ID
        # Notice the (?, ?, ?) -> These are placeholders for our variables
        worker.execute("""
            INSERT INTO products (name, price, brand_id) 
            VALUES (?, ?, ?)
        """, (product_name, price, brand_id))
        
        # 4. Save the changes!
        connection.commit()
        print(f"✅ Added {product_name} ({brand_name})")
    except sqlite3.IntegrityError:
        print(f"❌ Error: The product '{product_name}' already exists!")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# # Let's test it with some data
# add_product("RTX 4090", 1600.00, "Nvidia")
# add_product("RX 7900 XTX", 999.00, "AMD")
# add_product("RTX 3060", 350.00, "Nvidia")

def show_inventory():
    print("\n📦 CURRENT INVENTORY")
    print("-" * 50)

    # query the product name, price and brand name
    # use JOIN to see the brand name, not just the brand id
    query = """
    SELECT products.name, products.price, brands.name
    FROM products
    JOIN brands ON products.brand_id = brands.id
    """

    # run the query
    worker.execute(query)

    # fetch all results. gives a list of tuples
    all_rows = worker.fetchall()

    # check if the shop is empty
    if not all_rows:
        print("   (The inventory is empty)")
        return

    # loop through the shop items and print the results
    for row in all_rows:
        print(f"• {row[0]:<20} | ${row[1]:<10} | {row[2]}")
    
    print("-" * 50)

def search_product(keyword):
    print(f"\n🔎 SEARCH RESULTS FOR: '{keyword}'")
    print("-" * 50)

    query = """
    SELECT products.name, products.price, brands.name
    FROM products
    JOIN brands on products.brand_id = brands.id
    WHERE products.name LIKE ?
    """

    # use % symbols around the keyword for "fuzzy" matching
    search_term = f"%{keyword}%"

    worker.execute(query, (search_term,))
    rows = worker.fetchall()

    if not rows:
        print("   No products found.")
    else:
        for row in rows:
            print(f"• {row[0]:<20} | ${row[1]:<10} | {row[2]}")
            
    print("-" * 50)

def delete_product(product_name):
    # check if the product exists
    worker.execute("SELECT 1 FROM products WHERE name = ? ", (product_name, ))
    result = worker.fetchall()

    if not result:
        print(f"❌ Error: Product '{product_name}' not found.")
        return

    # when found, ask user for confirmation
    confirm = input(f"⚠️ Are you sure you want to delete '{product_name}'? (yes/no): ")

    if confirm.lower() == "yes":
        # delete the product
        worker.execute("DELETE FROM products WHERE name = ?", (product_name, ))
        connection.commit()
        print(f"✅ Deleted '{product_name}' successfully.")
    else:
        print("❌ Deletion cancelled.")



def start_app():
    # create the tables
    setup_tables()

    print("\n👋 Welcome to the Hardware Store Manager v1.0")

    # keep the app running in an infinite loop
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a Product")
        print("2. View Inventory")
        print("3. Search for a Product")
        print("4. Delete a Product") 
        print("5. Exit")

        # Get user choice
        choice = input("Enter number (1-5):")

        if choice == "1":
            try:
                # ask the user for details interactively
                product_name = input("Enter product name: ")
                raw_price = input("Enter price: ")
                product_brand = input("Enter brand name: ")

                # convert the price to a float
                product_price = float(raw_price)

                # check for logic errors
                if product_price < 0:
                    print("❌ Price cannot be negative!")
                    # skip to the next iteration
                    continue

                # pass the inputs to the add product function
                add_product(product_name, product_price, product_brand)
            except ValueError:
                print("❌ Error: Price must be a number (e.g., 10.99)")

        elif choice == "2":
            show_inventory()

        elif choice == "3":
            term = input("Enter search term (e.g, 'RTX'): ")
            search_product(term)

        elif choice == "4":
            p_name = input("Enter name of product to delete: ")
            delete_product(p_name)
            
        elif choice == "5":
             print("Goodbye!...")
             break

        else:
            print("❌ Invalid choice, please try again.")

start_app()