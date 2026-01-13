from sqlalchemy import create_engine, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

# --- 1. SETUP ---
class Base(DeclarativeBase):
    pass

# --- 2. MODELS ---
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # The List of Posts (One-to-Many)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    
    # The Link to the User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post '{self.title}'>"

# --- 3. CREATE DATABASE ---
engine = create_engine("sqlite:///blog.db") # echo=False for cleaner output
Base.metadata.create_all(engine)

# --- 4. LOGIC BLOCK ---
with Session(engine) as session:
    print("--- 1. GET OR CREATE USER ---")
    # Check if Alice exists
    stmt = select(User).where(User.name == "Alice")
    alice = session.scalar(stmt)

    if alice is None:
        print("🆕 Creating Alice...")
        alice = User(name="Alice")
        session.add(alice)
    else:
        print("👋 Found Alice.")

    print("--- 2. ADD POSTS ---")
    # Note: In a real app, we'd check if posts exist too, 
    # but for this demo, we'll just add them.
    post1 = Post(title="Hello World", user=alice)
    post2 = Post(title="SQLAlchemy is Cool", user=alice)
    
    session.add(post1)
    session.add(post2)
    session.commit()
    print("✅ Saved!")

# --- 5. VERIFY (READ) ---
with Session(engine) as session:
    print("\n--- 3. VERIFY RELATIONSHIPS ---")
    
    # We select Alice again
    stmt = select(User).where(User.name == "Alice")
    alice = session.scalar(stmt)
    
    print(f"User: {alice.name}")
    print(f"ID: {alice.id}")
    print(f"Posts: {alice.posts}") # <--- MAGIC MOMENT: This prints the list automatically!

with Session(engine) as session:
    print("\n--- RENAME AND DELETE ---")

    # 1. Select (Watch the Capital Letter!)
    stmt = select(User).where(User.name == "Alice")
    user = session.scalar(stmt)

    if user:
        # 2. Rename
        # We just change the variable. SQLAlchemy notices the change automatically.
        # This is called "Dirty Tracking".
        print(f"Renaming {user.name} to Alice Cooper...")
        user.name = "Alice Cooper"

        # 3. Delete a Post
        # We check if she actually has posts before trying to delete one
        if user.posts:
            post_to_delete = user.posts[0]
            print(f"Deleting post: '{post_to_delete.title}'")
            session.delete(post_to_delete)
        
        # 4. Commit
        # This saves the Name Change AND the Deletion
        session.commit()
        print("✅ Changes Saved!")
    else:
        print("❌ User not found!")
