import os
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from config import VOCAB_SIZE, MAX_LEN


class TokenizerManager:
    def __init__(self, frases=None, tokenizer_path: str = "saved/tokenizer.pkl"):
        self.tokenizer_path = tokenizer_path

        if frases:
            self.tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
            self.tokenizer.fit_on_texts(frases)
            self.save()
        else:
            self.tokenizer = self.load()

    def preparar(self, textos):
        secuencias = self.tokenizer.texts_to_sequences(textos)
        return pad_sequences(secuencias, maxlen=MAX_LEN, padding="post")

    def save(self):
        """Guarda el tokenizador en un archivo pickle"""
        os.makedirs(os.path.dirname(self.tokenizer_path), exist_ok=True)
        with open(self.tokenizer_path, "wb") as f:
            pickle.dump(self.tokenizer, f)
        print(f"💾 Tokenizer guardado en {self.tokenizer_path}")

    def load(self):
        """Carga un tokenizador guardado desde pickle"""
        if os.path.exists(self.tokenizer_path):
            with open(self.tokenizer_path, "rb") as f:
                print(f"📂 Tokenizer cargado desde {self.tokenizer_path}")
                return pickle.load(f)
        print(
            "⚠️ No se encontró un tokenizador guardado. Necesitás entrenar uno nuevo con frases base."
        )
        return None
