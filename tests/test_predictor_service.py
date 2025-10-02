from src.services.predictor_service import PredictorService

def test_predictor_service_predict():
    service = PredictorService()
    text = "Tengo miedo"
    prediction = service.predict(text)
    assert isinstance(prediction, dict)
    assert "emoción" in prediction or "emotion" in prediction