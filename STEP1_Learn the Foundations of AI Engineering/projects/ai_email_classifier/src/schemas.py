from pydantic import BaseModel, Field

class PriorityResult(BaseModel):
    """Result of priority classification"""
    priority: str = Field(description="Email priority: 'High', 'Medium', or 'Low'")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)

class CategoryResult(BaseModel):
    """Result of category classification"""
    category: str = Field(description="Email category: 'Work', 'Personal', 'Spam', 'Newsletter', 'Support', or 'Other'")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)

class EmailInfoResult(BaseModel):
    """Extracted information from email"""
    sender_intent: str = Field(description="The main intent or purpose of the email sender")
    action_required: bool = Field(description="Whether the email requires any action from the recipient")
    urgency_indicators: list[str] = Field(description="List of phrases or words that indicate urgency", default_factory=list)
    key_phrases: list[str] = Field(description="Important phrases or keywords extracted from the email", default_factory=list)