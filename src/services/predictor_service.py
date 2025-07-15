from model.emotion_model import EmotionModel
import numpy as np
import json
import os

class PredictorService:
    def __init__(self):
        self.model = EmotionModel()
        self.corrections_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'corrections.json')
        if not os.path.exists(self.corrections_path):
            with open(self.corrections_path, "w") as f:
                json.dump([], f)
        # Entrenamiento inicial con todas las correcciones
        with open(self.corrections_path, "r") as f:
            data = json.load(f)
        if data:
            X, y = self._preparar_datos(data)
            self.model.train(X, y)

    def vectorize(self, text):
        """Convierte el texto en un vector numérico fijo."""
        vec = [ord(c) for c in text][:100]
        vec += [0] * (100 - len(vec))
        return vec

    def predecir(self, texto):
        """Predice la emoción y confianza para un texto dado."""
        vector = self.vectorize(texto)
        emocion, confianza = self.model.predict(vector)
        return emocion, confianza

    def corregir(self, texto, emocion_correcta):
        """Guarda la corrección y reentrena el modelo con todas las correcciones."""
        with open(self.corrections_path, "r") as f:
            data = json.load(f)
        data.append({"texto": texto, "emocion": emocion_correcta})
        with open(self.corrections_path, "w") as f:
            json.dump(data, f)
        # Reentrena con todas las correcciones
        X, y = self._preparar_datos(data)
        self.model.train(X, y)

    def entrenar_con_correcciones(self, epochs=10):
        """Entrena el modelo con todas las correcciones guardadas."""
        with open(self.corrections_path, "r") as f:
            data = json.load(f)
        if data:
            X, y = self._preparar_datos(data)
            self.model.train(X, y, epochs=epochs)

    def _preparar_datos(self, data):
        """Prepara los datos X e y a partir de una lista de ejemplos."""
        X = [self.vectorize(d["texto"]) for d in data]
        y = []
        for d in data:
            label = [0] * len(self.model.labels)
            idx = self.model.labels.index(d["emocion"])
            label[idx] = 1
            y.append(label)
        return X, y
