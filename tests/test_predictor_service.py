from src.services.predictor_service import PredictorService

def test_predictor_service_predict():
    service = PredictorService()
    text = "Tengo miedo"
    prediction = service.predict_text(text)
    assert prediction is not None
    assert isinstance(prediction, (list, dict, str))