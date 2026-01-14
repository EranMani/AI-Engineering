from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

# create tables
# We access 'Base' via the models (models.Base) to ensure all tables are found
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/")
def create_user(user_data: schemas.UserSchema, db: Session = Depends(get_db)):
    print("creating user")
    stmt = select(models.UserDB).where(models.UserDB.name == user_data.name)
    existing_user = db.scalar(stmt)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.UserDB(name=user_data.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User createad!", "user_id": new_user.id, "name": new_user.name}

@app.get("/users/name/{user_name}")
def get_user_by_name(user_name: str, db: Session = Depends(get_db)):
    stmt = select(models.UserDB).where(models.UserDB.name == user_name)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(status_code=400, detail=f"User {user_name} not found!")

    return {"user_id": user.id, "name": user.name}

@app.post("/posts/")
def create_post(post_data: schemas.PostSchema, db: Session = Depends(get_db)):
    stmt = select(models.UserDB).where(models.UserDB.id == post_data.user_id)
    existing_user = db.scalar(stmt)

    if not existing_user:
        raise HTTPException(status_code=400, detail="User doesnt exist!")

    user_name = existing_user.name

    post = models.PostDB(title=post_data.title, user=existing_user)
    db.add(post)
    db.commit()

    return {"message": "Post created!", "post_title": post_data.title, "user_name": user_name}

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    stmt = select(models.UserDB)
    users = db.scalars(stmt).all()
    return users

@app.get("/")
def read_root():
    return {"message": "System Online", "status": "OK"}