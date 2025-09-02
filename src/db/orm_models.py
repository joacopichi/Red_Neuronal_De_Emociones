from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .database import Base

class EmotionResult(Base):
    __tablename__ = "emotion_results"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    predicted = Column(String(32), nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Correction(Base):
    __tablename__ = "corrections"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    # emoción correcta indicada por el usuario
    correct_emotion = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
