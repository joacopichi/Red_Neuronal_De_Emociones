from services.predictor_service import PredictorService
from config import CLASSES
import numpy as np

if __name__ == "__main__":
    ps = PredictorService()

    # 🔧 Cambia esto a "bd" si querés evaluar con los datos guardados en la base de datos
    modo = "bd"  # opciones: "demo" o "bd"

    if modo == "demo":
        ejemplos = [
            ("estoy muy enojado con vos", "ira"),
            ("me siento triste por lo que pasó", "tristeza"),
            ("qué alegría verte otra vez", "felicidad"),
            ("me asustó el ruido fuerte", "miedo"),
            ("no esperaba ese regalo", "sorpresa"),
            ("hoy es un día normal", "neutral"),
        ]
    else:
        print("📊 Cargando dataset desde la base de datos de feedback...")
        pares = ps.feedback.dataset()  # [(texto, label), ...]
        if not pares:
            print("⚠️ No hay feedback guardado en la BD para evaluar.")
            exit()
        ejemplos = pares

    # 🔎 Evaluación
    textos = [t for t, _ in ejemplos]
    etiquetas = [l for _, l in ejemplos]

    aciertos = 0
    for texto, etiqueta_real in ejemplos:
        pred, conf = ps.predecir(texto)
        ok = pred == etiqueta_real
        aciertos += int(ok)
        print(f"Texto: {texto}")
        print(f"   Real: {etiqueta_real} | Predicho: {pred} ({conf:.2f}) {'✅' if ok else '❌'}")

    print(f"\n📈 Accuracy: {aciertos}/{len(ejemplos)} = {aciertos/len(ejemplos):.2%}")
