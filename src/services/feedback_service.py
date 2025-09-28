from sqlalchemy.orm import Session
from db.database import db_singleton
from repositories.correction_repository import CorrectionRepository
from typing import List, Tuple, Optional, Dict

class FeedbackService:
    def __init__(self, db: Session = None):
        self.db = db if db else db_singleton.get_session()
        self.correction_repo = CorrectionRepository(self.db)
        
    def submit(self, texto: str, emocion_correcta: str) -> int:
        try:
            correction_id = self.correction_repo.save_correction(
                text=texto,
                correct_emotion=emocion_correcta,
            )
            print(f"✅ Feedback guardado: {texto[:50]}... -> {emocion_correcta}")
            return correction_id
        except Exception as e:
            print(f"❌ Error al guardar feedback: {e}")
            raise e
    
    def dataset(self) -> List[Tuple[str, str]]:
        try:
            corrections = self.correction_repo.get_all_corrections()
            return [(corr.text, corr.correct_emotion) for corr in corrections]
        except Exception as e:
            print(f"❌ Error al obtener dataset: {e}")
            return []
    
    def get_feedback_count(self) -> int:
        try:
            return self.correction_repo.count_corrections()
        except Exception as e:
            print(f"❌ Error al contar feedback: {e}")
            return 0
    
    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        try:
            corrections = self.correction_repo.get_recent_corrections(limit)
            return [
                {
                    "id": corr.id,
                    "text": corr.text,
                    "correct_emotion": corr.correct_emotion,
                    "created_at": corr.created_at
                }
                for corr in corrections
            ]
        except Exception as e:
            print(f"❌ Error al obtener feedback reciente: {e}")
            return []
    
    def get_correction_by_id(self, correction_id: int) -> Optional[Dict]:
        try:
            correction = self.correction_repo.get_correction_by_id(correction_id)
            if correction:
                return {
                    "id": correction.id,
                    "text": correction.text,
                    "correct_emotion": correction.correct_emotion,
                    "created_at": correction.created_at
                }
            return None
        except Exception as e:
            print(f"❌ Error al obtener corrección {correction_id}: {e}")
            return None
    
    def update_correction(self, correction_id: int, new_emotion: str) -> bool:
        try:
            success = self.correction_repo.update_correction(correction_id, new_emotion)
            if success:
                print(f"✅ Corrección {correction_id} actualizada -> {new_emotion}")
            return success
        except Exception as e:
            print(f"❌ Error al actualizar corrección {correction_id}: {e}")
            return False
    
    def delete_correction(self, correction_id: int) -> bool:
        try:
            success = self.correction_repo.delete_correction(correction_id)
            if success:
                print(f"✅ Corrección {correction_id} eliminada")
            return success
        except Exception as e:
            print(f"❌ Error al eliminar corrección {correction_id}: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        try:
            stats = self.correction_repo.get_feedback_statistics()
            return stats
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return {
                "total_corrections": 0,
                "emotions_distribution": {},
                "recent_activity": []
            }
    
    def guardar_feedback(self, texto: str, emocion_real: str, emocion_predicha: str, db: Session = None) -> int:
        return self.submit(texto, emocion_real)