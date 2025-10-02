import numpy as np
from src.model.emotion_model import EmotionModel

def test_model_predict_returns_numpy_array():
    model = EmotionModel(vocab_size=5000, num_classes=6, max_len=100)
    input_shape = model.model.input_shape
    max_len = input_shape[1]
    dummy_input = np.zeros((2, max_len))
    preds = model.model.predict(dummy_input)
    assert isinstance(preds, np.ndarray)
    assert preds.shape[0] == 2
    assert preds.shape[1] == model.num_classes