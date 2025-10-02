VOCAB_SIZE = 1000
MAX_LEN = 10
EMBEDDING_DIM = 16
NUM_CLASSES = 6
EPOCHS = 15
CLASSES = {
    0: "ira",
    1: "tristeza",
    2: "felicidad",
    3: "sorpresa",
    4: "miedo",
    5: "neutral",
}
CLASSES_REVERSE = {
    "ira": 0,
    "tristeza": 1,
    "felicidad": 2,
    "sorpresa": 3,
    "miedo": 4,
    "neutral": 5,
}
DATABASE_URL = "sqlite:///red_emociones.db"
