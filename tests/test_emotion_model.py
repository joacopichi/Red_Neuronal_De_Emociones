from src.model.emotion_model import EmotionModel

def test_model_predict_returns_list():
    model = EmotionModel(vocab_size=5000, num_classes=6, max_len=100)
    sample_texts = ["Estoy feliz", "Tengo miedo"]
    preds = model.predict(sample_texts)
    assert isinstance(preds, list)
    assert len(preds) == len(sample_texts)