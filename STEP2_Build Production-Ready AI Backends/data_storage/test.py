import sqlite3

# create a connection to the database
connection = sqlite3.connect("library.db")
# create the worker to handle tasks
worker = connection.cursor()

def setup_database():
    # create authors table
    worker.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    # create books table
    worker.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, author_id INTEGER REFERENCES authors(id))")

def add_book(title, year, author_name):
    try:
        # 1. Ensure author exists
        # Note the comma! (author_name,)
        worker.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author_name,))
        
        # 2. Get the ID
        # Note the comma again!
        result = worker.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
        
        # We use fetchone() because we know there is only one ID for this name.
        # [0] grabs the number '1' from the tuple (1,)
        author_id = result.fetchone()[0]

        # 3. Insert the book
        worker.execute("INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)", 
                       (title, year, author_id))

        connection.commit()
        print(f"✅ Added '{title}' by {author_name}")
        
    except sqlite3.IntegrityError:
        # This will only trigger if 'books.id' conflicts (rare) or if you made 'books.title' UNIQUE.
        print(f"❌ Error: The book '{title}' might already exist.")
        
    except Exception as e:
        print(f"❌ unexpected error: {e}")


def show_catalog():
    query = """
    SELECT books.title, books.year, authors.name
    FROM books
    JOIN authors ON books.author_id = authors.id
    """

    # run the show query command
    worker.execute(query)

    all_rows = worker.fetchall()

    if not all_rows:
        print("There are no books at the current moment! Please return later.")
        return

    for row in all_rows:
        print(f"{row[1]} | {row[0]} | {row[2]}")


