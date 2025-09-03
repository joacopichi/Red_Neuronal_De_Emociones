from sqlalchemy.orm import Session
from db.database import db_singleton
from repositories.emotion_repository import EmotionRepository
from services.feedback_service import FeedbackService

from data.base_data import BaseDataManager
from model.tokenizer_manager import TokenizerManager
from model.emotion_model import EmotionModel
from config import CLASSES, CLASSES_REVERSE, MAX_LEN

import numpy as np
import os

LABELS = ["ira", "tristeza", "felicidad", "sorpresa", "miedo", "neutral"]


class PredictorService:
    def __init__(self):
        self.db: Session = db_singleton.get_session()
        self.pred_repo = EmotionRepository(self.db)
        self.feedback = FeedbackService(self.db)

        # Datos base
        self.base = BaseDataManager()
        frases_base, y_base_idx = self.base.obtener_datos()

        # --- Tokenizer ---
        self.tokenizer = TokenizerManager()  # intenta cargar desde saved
        if self.tokenizer.tokenizer is None:
            print("🚀 Creando y entrenando nuevo Tokenizer...")
            self.tokenizer = TokenizerManager(frases_base)

        # --- Modelo ---
        self.model = EmotionModel(
            vocab_size=self.tokenizer.tokenizer.num_words,
            num_classes=len(LABELS),
            max_len=MAX_LEN
        )

        if not os.path.exists("saved/model.keras"):
            print("🚀 Entrenando modelo por primera vez con datos base...")
            Xb = self.tokenizer.preparar(frases_base)
            yb = np.array(y_base_idx, dtype=np.int32)
            self.model.train(Xb, yb, epochs=3)

        # Ajustar con feedback acumulado
        self.entrenar_con_correcciones(epochs=2)

    def predecir(self, texto: str):
        seq = self.tokenizer.preparar([texto])
        probs = self.model.predict_proba(seq)[0]
        idx = int(np.argmax(probs))
        pred = LABELS[idx]
        conf = float(probs[idx])

        # Guardar predicción en BD
        self.pred_repo.save_prediction(text=texto, predicted=pred, confidence=conf)
        return pred, conf

    def corregir(self, texto: str, emocion_correcta: str):
        # Guardar feedback en BD
        self.feedback.submit(texto, emocion_correcta)
        # Reentrenamiento corto inmediato
        self.entrenar_con_correcciones(epochs=2)

    def entrenar_con_correcciones(self, epochs=3, reentrenar_desde_cero=False):
        """
        Reentrena el modelo con los datos de feedback de la BD.
        Si reentrenar_desde_cero=True, el modelo se reinicia y se entrena desde cero
        usando base_data + feedback acumulado.
        """
        pares = self.feedback.dataset()  # [(texto, label), ...]
        if not pares:
            print("⚠️ No hay datos de feedback para reentrenar.")
            return

        textos = [t for t, _ in pares]
        labels = [CLASSES_REVERSE.get(l, 5) for _, l in pares]  # default neutral si no mapea

        if reentrenar_desde_cero:
            print("🔄 Reentrenando modelo desde cero con base + feedback...")

            frases_base, y_base_idx = self.base.obtener_datos()
            self.tokenizer = TokenizerManager(frases_base + textos)

            self.model = EmotionModel(
                vocab_size=self.tokenizer.tokenizer.num_words,
                num_classes=len(LABELS),
                max_len=MAX_LEN
            )

            # Unimos base + feedback
            X_base = self.tokenizer.preparar(frases_base)
            y_base = np.array(y_base_idx, dtype=np.int32)

            X_feedback = self.tokenizer.preparar(textos)
            y_feedback = np.array(labels, dtype=np.int32)

            X = np.concatenate([X_base, X_feedback], axis=0)
            y = np.concatenate([y_base, y_feedback], axis=0)

            self.model.train(X, y, epochs=epochs)
        else:
            # Solo entrenamos con feedback nuevo
            print("📈 Ajustando modelo con feedback...")
            X = self.tokenizer.preparar(textos)
            y = np.array(labels, dtype=np.int32)
            self.model.train(X, y, epochs=epochs)
