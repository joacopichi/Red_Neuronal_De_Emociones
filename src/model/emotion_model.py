import tensorflow as tf
import numpy as np

class EmotionModel:
    def __init__(self):
        self.labels = ["ira", "tristeza", "felicidad", "sorpresa", "miedo", "neutral"]
        try:
            self.model = tf.keras.models.load_model("modelo.keras")
        except Exception:
            self.model = self._build_model()
            self.model.save("modelo.keras")

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(16, activation='relu', input_shape=(100,)),
            tf.keras.layers.Dense(len(self.labels), activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def predict(self, vector):
        pred = self.model.predict(np.array([vector]))[0]
        idx = np.argmax(pred)
        return self.labels[idx], float(pred[idx])

    def train(self, X, y):
        self.model.fit(np.array(X), np.array(y), epochs=10, verbose=0)
        self.model.save("modelo.keras")
