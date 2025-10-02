from .base_repository import BaseRepository
from db.orm_models import EmotionResult
from sqlalchemy.orm import Session


class EmotionRepository(BaseRepository[EmotionResult]):
    def __init__(self, db: Session):
        super().__init__(EmotionResult, db)

    def save_prediction(
        self, text: str, predicted: str, confidence: float
    ) -> EmotionResult:
        rec = EmotionResult(text=text, predicted=predicted, confidence=confidence)
        return self.add(rec)
