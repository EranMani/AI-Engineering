from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str

class PostSchema(BaseModel):
    title: str
    user_id: int