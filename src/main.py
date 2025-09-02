from services.predictor_service import PredictorService

if __name__ == "__main__":
    ps = PredictorService()

    print("Escribe frases para predecir emociones (ira, tristeza, felicidad, sorpresa, miedo, neutral).")
    print("Escribe 'salir' para terminar.\n")

    while True:
        texto = input("Texto: ").strip()
        if not texto:
            continue
        if texto.lower() == "salir":
            break

        emocion, confianza = ps.predecir(texto)
        print(f"🤖 Predicción: {emocion.upper()}  (confianza: {confianza:.2f})")

        ok = input("¿Es correcta la emoción? (s/n): ").strip().lower()
        if ok == "n":
            correcta = input("¿Cuál es la emoción correcta? (ira, tristeza, felicidad, sorpresa, miedo, neutral): ").strip().lower()
            ps.corregir(texto, correcta)
            print("✅ Corrección guardada y modelo ajustado.\n")
        else:
            print("👍 Genial.\n")
