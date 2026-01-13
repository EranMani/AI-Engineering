from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

# database setup
engine = create_engine("sqlite:///api_database.db", echo=True)

class Base(DeclarativeBase):
    pass

# the sqlalchemy model (the table)
class UserDB(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    posts: Mapped[list["PostDB"]] = relationship(back_populates="user")

class PostDB(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDB"] = relationship(back_populates="posts")

# create the table
Base.metadata.create_all(engine)

# pydantic schemas
class UserSchema(BaseModel):
    name: str

class PostSchema(BaseModel):
    title: str
    user_id: int

# fastapi server setup
app = FastAPI()

# the dependency
# open a session for a request, and close it when done
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

@app.post("/users/")
def create_user(user_data: UserSchema, db: Session=Depends(get_db)):
    # check if user exists
    stmt = select(UserDB).where(UserDB.name == user_data.name)
    existing_user = db.scalar(stmt)
    print(existing_user)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # create new sql alchemy object
    new_user = UserDB(name=user_data.name)

    db.add(new_user)
    db.commit()
    # get the ID back from the database
    db.refresh(new_user)

    return {"message": "User created", "user_id": new_user.id, "name": new_user.name}

@app.post("/posts/")
def create_post(post_data: PostSchema, db: Session = Depends(get_db)):
    # check if user exists in DB
    stmt = select(UserDB).where(UserDB.id == post_data.user_id)
    existing_user = db.scalar(stmt)
    
    if not existing_user:
        raise HTTPException(status_code=400, detail="User doesnt exist!")

    user_name = existing_user.name

    post = PostDB(title=post_data.title, user=existing_user)
    db.add(post)
    db.commit()

    return {"message": "Post created", "post_title": post_data.title, "user_name": user_name}

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    stmt = select(UserDB)
    users = db.scalars(stmt).all()
    return users

@app.get("/users/name/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    # search for the user in DB
    stmt = select(UserDB).where(UserDB.name == user_name)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=400, detail=f"User {user} not found!")

    return {"user_id": user.id, "name": user.name}

# the route
@app.get("/")
def read_root():
    # the response
    return {"message": "Hello world", "status": "Online"}
