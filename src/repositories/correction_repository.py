from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from db.orm_models import Correction
from typing import List, Optional, Dict
from datetime import datetime


class CorrectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_correction(self, text: str, correct_emotion: str) -> int:
        try:
            correction = Correction(
                text=text, correct_emotion=correct_emotion, created_at=datetime.now()
            )

            self.db.add(correction)
            self.db.commit()
            self.db.refresh(correction)

            return correction.id
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_corrections(self) -> List[Correction]:
        try:
            return self.db.query(Correction).all()
        except Exception as e:
            print(f"Error al obtener correcciones: {e}")
            return []

    def get_recent_corrections(self, limit: int = 10) -> List[Correction]:
        try:
            return (
                self.db.query(Correction)
                .order_by(desc(Correction.created_at))
                .limit(limit)
                .all()
            )
        except Exception as e:
            print(f"Error al obtener correcciones recientes: {e}")
            return []

    def get_correction_by_id(self, correction_id: int) -> Optional[Correction]:
        try:
            return (
                self.db.query(Correction).filter(Correction.id == correction_id).first()
            )
        except Exception as e:
            print(f"Error al obtener corrección {correction_id}: {e}")
            return None

    def update_correction(self, correction_id: int, new_emotion: str) -> bool:
        try:
            correction = self.get_correction_by_id(correction_id)
            if correction:
                correction.correct_emotion = new_emotion
                correction.updated_at = datetime.now()
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error al actualizar corrección {correction_id}: {e}")
            return False

    def delete_correction(self, correction_id: int) -> bool:
        try:
            correction = self.get_correction_by_id(correction_id)
            if correction:
                self.db.delete(correction)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error al eliminar corrección {correction_id}: {e}")
            return False

    def count_corrections(self) -> int:
        try:
            return self.db.query(Correction).count()
        except Exception as e:
            print(f"Error al contar correcciones: {e}")
            return 0

    def get_feedback_statistics(self) -> Dict:
        try:
            total = self.count_corrections()

            emotion_stats = (
                self.db.query(
                    Correction.correct_emotion, func.count(Correction.id).label("count")
                )
                .group_by(Correction.correct_emotion)
                .all()
            )

            emotions_distribution = {emotion: count for emotion, count in emotion_stats}

            recent = self.get_recent_corrections(10)
            recent_activity = [
                {
                    "id": corr.id,
                    "text": (
                        corr.text[:50] + "..." if len(corr.text) > 50 else corr.text
                    ),
                    "emotion": corr.correct_emotion,
                    "created_at": str(corr.created_at),
                }
                for corr in recent
            ]

            return {
                "total_corrections": total,
                "emotions_distribution": emotions_distribution,
                "recent_activity": recent_activity,
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                "total_corrections": 0,
                "emotions_distribution": {},
                "recent_activity": [],
            }

    def get_corrections_by_user(self, int) -> List[Correction]:
        try:
            return self.db.query(Correction).order_by(desc(Correction.created_at)).all()
        except Exception as e:
            print(f"Error al obtener correcciones del usuario : {e}")
            return []

    def get_corrections_by_emotion(self, emotion: str) -> List[Correction]:
        try:
            return (
                self.db.query(Correction)
                .filter(Correction.correct_emotion == emotion)
                .order_by(desc(Correction.created_at))
                .all()
            )
        except Exception as e:
            print(f"Error al obtener correcciones para emoción {emotion}: {e}")
            return []
