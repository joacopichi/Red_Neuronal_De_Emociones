from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from config import VOCAB_SIZE, MAX_LEN

class TokenizerManager:
    def __init__(self, frases):
        self.tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(frases)

    def preparar(self, textos):
        secuencias = self.tokenizer.texts_to_sequences(textos)
        return pad_sequences(secuencias, maxlen=MAX_LEN, padding='post')
