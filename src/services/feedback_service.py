from sqlalchemy.orm import Session
from repositories.correction_repository import CorrectionRepository

class FeedbackService:
    def __init__(self, db: Session):
        self.repo = CorrectionRepository(db)

    def submit(self, text: str, correct_emotion: str):
        return self.repo.save_correction(text, correct_emotion)

    def dataset(self):
        return self.repo.all_texts_and_labels()
