import tensorflow as tf

class EmotionModel:
    def __init__(self, vocab_size: int, num_classes: int, max_len: int, model_path: str = "modelo.keras"):
        self.vocab_size = max(vocab_size or 1000, 1000)  # por si vocab_size= None
        self.num_classes = num_classes
        self.max_len = max_len
        self.model_path = model_path
        try:
            self.model = tf.keras.models.load_model(self.model_path)
        except Exception:
            self.model = self._build_model()
            self.model.save(self.model_path)

    def _build_model(self):
        inputs = tf.keras.Input(shape=(self.max_len,), dtype="int32")
        x = tf.keras.layers.Embedding(input_dim=self.vocab_size, output_dim=64, input_length=self.max_len)(inputs)
        x = tf.keras.layers.GlobalAveragePooling1D()(x)
        x = tf.keras.layers.Dense(64, activation="relu")(x)
        outputs = tf.keras.layers.Dense(self.num_classes, activation="softmax")(x)
        model = tf.keras.Model(inputs, outputs)
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        return model

    def train(self, X, y, epochs=3, batch_size=16):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
        self.model.save(self.model_path)

    def predict_proba(self, X):
        return self.model.predict(X, verbose=0)
