from dataclasses import field
from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(description="The emotional tone: 'Positive', 'Negative', or 'Neutral'")
    score: float = Field(description="Confidence score between 0.0 and 1.0")
    key_points: list[str] = Field(description="Bullet point extracting the main topics")

class UserRequset(BaseModel):
    message: str