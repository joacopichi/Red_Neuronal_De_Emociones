import threading
import time
import os
from emotion_classifier.services.predictor_service import PredictorService

def entrenamiento_automatico(ps, path, intervalo=10):
    """Entrena el modelo solo si el archivo de correcciones cambia."""
    last_mtime = os.path.getmtime(path)
    while True:
        time.sleep(intervalo)
        current_mtime = os.path.getmtime(path)
        if current_mtime != last_mtime:
            ps.entrenar_con_correcciones()
            print("Entrenamiento automático realizado por cambio en correcciones.")
            last_mtime = current_mtime

print("Analizador de emociones\nEscribí una frase. Escribí 'salir' para terminar.\n")
ps = PredictorService()
corrections_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'corrections.json')
corrections_dir = os.path.dirname(corrections_path)
if not os.path.exists(corrections_dir):
    os.makedirs(corrections_dir)
if not os.path.exists(corrections_path):
    with open(corrections_path, "w") as f:
        f.write("[]")

# Inicia el entrenamiento automático eficiente en segundo plano
hilo_entrenamiento = threading.Thread(
    target=entrenamiento_automatico, args=(ps, corrections_path, 10), daemon=True
)
hilo_entrenamiento.start()

while True:
    texto = input("Texto: ")
    if texto.lower() == "salir":
        break
    emocion, confianza = ps.predecir(texto)
    print(f"Predicción: {emocion.upper()} (confianza: {confianza:.2f})")
    ok = input("¿Es correcta la emoción? (s/n): ").lower()
    if ok == "n":
        correcta = input("¿Cuál es la emoción correcta? (ira, tristeza, felicidad, sorpresa, miedo, neutral): ").lower()
        ps.corregir(texto, correcta)
        print("Corrección guardada y modelo actualizado.\n")
    else:
        print()