from services.predictor_service import PredictorService


def retrain_model_background(epochs: int = 50, from_scratch: bool = False):
    predictor = PredictorService()
    modo = "desde cero" if from_scratch else "incremental"
    print(f"🚀 Reentrenando modelo ({modo}, epochs={epochs})")
    predictor.entrenar_con_correcciones(
        epochs=epochs, reentrenar_desde_cero=from_scratch
    )
    print("✅ Reentrenamiento completado")
