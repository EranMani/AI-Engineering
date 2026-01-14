from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str

class PostSchema(BaseModel):
    title: str
    content: Optional[str] = None # optional means it can be empty
    user_id: int