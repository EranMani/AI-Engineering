from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

# --- Setup & Class Definition (Keep this exactly the same) ---
class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    price: Mapped[float] = mapped_column()

engine = create_engine("sqlite:///orm_store.db", echo=True)
Base.metadata.create_all(engine)

# --- ❌ DELETED THE UNSAFE "ADDING DATA" BLOCK HERE ---

# --- ✅ SMART INSERT (Safe to run multiple times) ---
with Session(engine) as session:
    print("\n--- SMART INSERT ---")

    # We combine ALL items here (Old duplicates + New items)
    items_to_add = [
        {"name": "Nvidia RTX 4090", "price": 1600.00}, # Exists? Will ignore.
        {"name": "Intel Core i9", "price": 550.50},    # Exists? Will ignore.
        {"name": "Gaming Mouse", "price": 45.00},      # New? Will add.
        {"name": "Mechanical Keyboard", "price": 120.00} # New? Will add.
    ]

    for item in items_to_add:
        # 1. Build the Insert
        stmt = sqlite_insert(Product).values(name=item["name"], price=item["price"])
        
        # 2. Add the Safety Shield 🛡️
        stmt = stmt.on_conflict_do_nothing(index_elements=['name'])
        
        # 3. Execute
        session.execute(stmt)

    session.commit()
    print("--- Data Synced Successfully ---")

# --- READ INVENTORY ---
with Session(engine) as session:
    print("\n--- CURRENT INVENTORY ---")
    results = session.scalars(select(Product))
    for item in results:
        print(f"ID: {item.id} | Name: {item.name} | Price: ${item.price}")