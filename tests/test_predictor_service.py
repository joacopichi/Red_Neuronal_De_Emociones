from src.services.predictor_service import PredictorService

def test_predictor_service_predecir():
    service = PredictorService()
    text = "Tengo miedo"
    pred, conf = service.predecir(text)

    assert isinstance(pred, str)
    assert isinstance(conf, float)
    assert 0.0 <= conf <= 1.0