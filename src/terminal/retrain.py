from services.predictor_service import PredictorService

if __name__ == "__main__":
    ps = PredictorService()

    ps.entrenar_con_correcciones(epochs=50, reentrenar_desde_cero=True)

    print("✅ Reentrenamiento completo usando todos los datos históricos")
