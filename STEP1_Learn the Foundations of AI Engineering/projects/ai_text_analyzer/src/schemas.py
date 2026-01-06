from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(description="The sentiment: 'Positive', 'Negative' or 'neutral'")
    score: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)

class SummaryResult(BaseModel):
    summary: str = Field(description="A concise summary of the text")
    key_points: list[str] = Field(description="List of key points extracted")

class TopicResult(BaseModel):
    topics: list[str] = Field(description="List of main topics identified")
    primary_topic: str = Field(description="The most prominent topic")