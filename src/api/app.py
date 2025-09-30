from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import sys

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from services.predictor_service import PredictorService
    from services.feedback_service import FeedbackService
    from db.database import db_singleton
    services_available = True
    print("✅ Servicios importados correctamente")
except ImportError as e:
    print(f"❌ Error importando servicios: {e}")
    services_available = False

app = FastAPI(
    title="API de Red Neuronal de Emociones",
    description="Predice emociones, permite corrección y reentrenamiento",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    emotion: str
    confidence: float
    feedback_id: Optional[int] = None

class FeedbackInput(BaseModel):
    text: str
    predicted_emotion: str
    corrected_emotion: str

class FeedbackUpdate(BaseModel):
    corrected_emotion: str

class FeedbackItem(BaseModel):
    id: int
    text: str
    predicted_emotion: str
    corrected_emotion: str
    created_at: Optional[str] = None

class TrainResponse(BaseModel):
    message: str
    status: str

predictor = None
feedback_service = None

if services_available:
    try:
        predictor = PredictorService()
        feedback_service = FeedbackService()
        print("✅ Servicios inicializados correctamente")
    except Exception as e:
        print(f"❌ Error inicializando servicios: {e}")
        services_available = False

@app.get("/", response_class=HTMLResponse)
async def root():
    status = "✅ Funcionando" if services_available else "❌ Error en servicios"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Red Neuronal de Emociones</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; }}
            h1 {{ text-align: center; }}
            label {{ display: block; margin-top: 15px; }}
            input, select, button, textarea {{ width: 100%; padding: 8px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc; }}
            button {{ background: #007bff; color: white; font-weight: bold; cursor: pointer; }}
            button:hover {{ background: #0056b3; }}
            .result {{ margin-top: 20px; padding: 15px; border-radius: 5px; background: #e9ecef; }}
            #volverBtn {{ background: #28a745; margin-top: 10px; }}
            #volverBtn:hover {{ background: #1e7e34; }}
            .status {{ background: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #155724; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Predicción de Emociones</h1>
            <div class="status"><strong>Estado del sistema:</strong> {status}</div>

            <label for="textInput">Escribe un texto:</label>
            <textarea id="textInput" rows="3"></textarea>

            <button type="button" onclick="predictEmotion()">Predecir Emoción</button>

            <div id="prediction" class="result" style="display:none;">
                <p><strong>Predicción:</strong> <span id="predictedEmotion"></span></p>
                <p><strong>Confianza:</strong> <span id="confidence"></span></p>

                <label for="correctEmotion">¿Es correcta la emoción? (opcional, corrígela si es necesario)</label>
                <select id="correctEmotion">
                    <option value="">-- Selecciona si quieres corregir --</option>
                    <option value="ira">Ira</option>
                    <option value="tristeza">Tristeza</option>
                    <option value="felicidad">Felicidad</option>
                    <option value="sorpresa">Sorpresa</option>
                    <option value="miedo">Miedo</option>
                    <option value="neutral">Neutral</option>
                </select>

                <button type="button" onclick="sendFeedback()">Enviar Feedback</button>
                <p id="feedbackMsg" style="color: green; font-weight:bold;"></p>
                <button type="button" id="volverBtn" onclick="resetForm()">Volver a preguntar</button>
            </div>
        </div>

        <script>
            let lastPrediction = null;

            async function predictEmotion() {{
                const text = document.getElementById("textInput").value.trim();
                if (!text) return alert("Escribe algo para predecir.");

                const response = await fetch("/predict_feedback", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ text }})
                }});

                const data = await response.json();
                lastPrediction = data;

                document.getElementById("predictedEmotion").textContent = data.emotion;
                document.getElementById("confidence").textContent = data.confidence.toFixed(2);
                document.getElementById("prediction").style.display = "block";
                document.getElementById("feedbackMsg").textContent = "";
            }}

            async function sendFeedback() {{
                const corrected = document.getElementById("correctEmotion").value;
                if (!corrected) return alert("Selecciona una emoción corregida antes de enviar.");

                const text = document.getElementById("textInput").value.trim();

                const response = await fetch("/predict_feedback?corrected_emotion=" + corrected, {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ text }})
                }});

                const data = await response.json();
                document.getElementById("feedbackMsg").textContent = "✅ Feedback registrado. ID: " + data.feedback_id;
            }}

            function resetForm() {{
                document.getElementById("textInput").value = "";
                document.getElementById("predictedEmotion").textContent = "";
                document.getElementById("confidence").textContent = "";
                document.getElementById("correctEmotion").selectedIndex = 0;
                document.getElementById("feedbackMsg").textContent = "";
                document.getElementById("prediction").style.display = "none";
                lastPrediction = null;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/predict_feedback", response_model=PredictionResponse)
async def predict_feedback(
    input_data: TextInput,
    background_tasks: BackgroundTasks,
    corrected_emotion: Optional[str] = None
):
    if not services_available or not predictor or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicios no disponibles")
    
    try:
        emotion, confidence = predictor.predecir(input_data.text)
        feedback_id = None

        if corrected_emotion:
            feedback_id = feedback_service.submit(input_data.text, corrected_emotion)
            background_tasks.add_task(retrain_model_background, epochs=5, from_scratch=False)

        return PredictionResponse(
            emotion=emotion,
            confidence=confidence,
            feedback_id=feedback_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")


@app.get("/feedback", response_model=List[FeedbackItem])
async def get_feedback():
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    corrections = feedback_service.get_recent_feedback(limit=100)
    return [
        FeedbackItem(
            id=corr.get("id", 0),
            text=corr.get("text", ""),
            predicted_emotion=corr.get("predicted_emotion", ""),
            corrected_emotion=corr.get("correct_emotion", ""),
            created_at=str(corr.get("created_at", "")) if corr.get("created_at") else None
        )
        for corr in corrections
    ]

@app.put("/feedback/{feedback_id}", response_model=FeedbackItem)
async def update_feedback(feedback_id: int, update_data: FeedbackUpdate):
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    success = feedback_service.update_correction(feedback_id, update_data.corrected_emotion)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    
    updated = feedback_service.get_correction_by_id(feedback_id)
    return FeedbackItem(
        id=updated["id"],
        text=updated["text"],
        predicted_emotion=updated.get("predicted_emotion", ""),
        corrected_emotion=updated.get("correct_emotion", "")
    )

@app.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int):
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    success = feedback_service.delete_correction(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    
    return {"message": "Feedback eliminado correctamente"}

@app.post("/train", response_model=TrainResponse)
async def train_model(
    background_tasks: BackgroundTasks,
    epochs: int = 50,
    from_scratch: bool = False
):
    if not services_available or not predictor:
        raise HTTPException(status_code=503, detail="Servicio de predicción no disponible")
    
    background_tasks.add_task(retrain_model_background, epochs=epochs, from_scratch=from_scratch)
    return TrainResponse(message="Entrenamiento completo iniciado en segundo plano", status="started")


def retrain_model_background(epochs: int = 50, from_scratch: bool = False):
    try:
        modo = "desde cero" if from_scratch else "incremental"
        print(f"🚀 Reentrenando modelo ({modo}, epochs={epochs})")
        predictor.entrenar_con_correcciones(epochs=epochs, reentrenar_desde_cero=from_scratch)
        print("✅ Reentrenamiento completado")
    except Exception as e:
        print(f"❌ Error en reentrenamiento: {e}")

@app.get("/health")
async def health_check():
    return {
        "status": "ok" if services_available else "error",
        "services": {
            "predictor": predictor is not None,
            "feedback": feedback_service is not None,
            "database": db_singleton is not None if 'db_singleton' in globals() else False
        },
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)