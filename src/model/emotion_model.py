import os
import tensorflow as tf


class EmotionModel:
    def __init__(
        self,
        vocab_size: int,
        num_classes: int,
        max_len: int,
        model_path: str = "saved/emotion_model.keras",
        reentrenar_desde_cero: bool = False,
    ):
        self.vocab_size = max(vocab_size or 1000, 1000)  # por si vocab_size=None
        self.num_classes = num_classes
        self.max_len = max_len
        self.model_path = model_path

        if not reentrenar_desde_cero and os.path.exists(self.model_path):
            print(f"📂 Cargando modelo existente desde {self.model_path}")
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            print(
                "⚠️ No se encontró modelo o se solicitó reentrenar desde cero. Construyendo nuevo modelo..."
            )
            self.model = self._build_model()
            self.save()

    def _build_model(self):
        inputs = tf.keras.Input(shape=(self.max_len,), dtype="int32")
        x = tf.keras.layers.Embedding(
            input_dim=self.vocab_size, output_dim=64, input_length=self.max_len
        )(inputs)
        x = tf.keras.layers.GlobalAveragePooling1D()(x)
        x = tf.keras.layers.Dense(64, activation="relu")(x)
        outputs = tf.keras.layers.Dense(self.num_classes, activation="softmax")(x)
        model = tf.keras.Model(inputs, outputs)
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return model

    def train(self, X, y, epochs=3, batch_size=16):
        """Entrena y guarda automáticamente el modelo"""
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)
        self.save()

    def predict_proba(self, X):
        return self.model.predict(X, verbose=0)

    def save(self):
        """Guarda el modelo en el path definido"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"💾 Modelo guardado en {self.model_path}")

    @staticmethod
    def load(path="saved/emotion_model.keras"):
        """Carga un modelo guardado"""
        if os.path.exists(path):
            print(f"📂 Cargando modelo desde {path}")
            model = tf.keras.models.load_model(path)
            wrapper = EmotionModel(
                vocab_size=1, num_classes=1, max_len=1, model_path=path
            )
            wrapper.model = model
            return wrapper
        print(f"⚠️ No se encontró modelo en {path}")
        return None
