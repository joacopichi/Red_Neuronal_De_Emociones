from src.model.emotion_model import EmotionModel

def test_model_predict_returns_list():
    model = EmotionModel()
    sample_text = ["Estoy feliz"]
    result = model.predict(sample_text)
    assert isinstance(result, list)
    assert len(result) == 1