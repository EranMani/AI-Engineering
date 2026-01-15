from pydantic import BaseModel

class VoteCreate(BaseModel):
    candidate_name: str

class VoteResponse(BaseModel):
    id: int
    candidate_name: str
    message: str