from pydantic import BaseModel
from typing import Optional

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    emotion: str
    confidence: float
    feedback_id: Optional[int] = None

class FeedbackInput(BaseModel):
    text: str
    predicted_emotion: str
    corrected_emotion: str

class FeedbackUpdate(BaseModel):
    corrected_emotion: str

class FeedbackItem(BaseModel):
    id: int
    text: str
    predicted_emotion: str
    corrected_emotion: str
    created_at: Optional[str] = None

class TrainResponse(BaseModel):
    message: str
    status: str
