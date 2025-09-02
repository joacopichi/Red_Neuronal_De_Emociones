from .base_repository import BaseRepository
from db.orm_models import Correction
from sqlalchemy.orm import Session
from typing import List

class CorrectionRepository(BaseRepository[Correction]):
    def __init__(self, db: Session):
        super().__init__(Correction, db)

    def save_correction(self, text: str, correct_emotion: str) -> Correction:
        rec = Correction(text=text, correct_emotion=correct_emotion)
        return self.add(rec)

    def all_texts_and_labels(self) -> list[tuple[str, str]]:
        rows: List[Correction] = self.db.query(Correction).all()
        return [(r.text, r.correct_emotion) for r in rows]
