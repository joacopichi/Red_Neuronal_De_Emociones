from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
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
    description="API para predecir emociones en texto y gestionar feedback",
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

class FeedbackInput(BaseModel):
    text: str
    predicted_emotion: str
    corrected_emotion: str
    user_id: Optional[int] = None

class FeedbackResponse(BaseModel):
    message: str
    id: int

class FeedbackItem(BaseModel):
    id: int
    text: str
    emotion: Optional[str] = None
    corrected_emotion: str
    user_id: Optional[int] = None
    created_at: Optional[str] = None

class FeedbackUpdate(BaseModel):
    corrected_emotion: str

class TrainResponse(BaseModel):
    message: str
    status: str

predictor = None
feedback_service = None

if services_available:
    try:
        print("🚀 Inicializando PredictorService...")
        predictor = PredictorService()
        print("✅ PredictorService inicializado")
        
        print("🚀 Inicializando FeedbackService...")
        feedback_service = FeedbackService()
        print("✅ FeedbackService inicializado")
    except Exception as e:
        print(f"❌ Error al inicializar servicios: {e}")
        services_available = False

@app.get("/", response_class=HTMLResponse)
async def root():
    status = "✅ Funcionando" if services_available else "❌ Error en servicios"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Red Neuronal de Emociones</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .endpoint {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
            .status {{ background: #d4edda; padding: 15px; margin: 20px 0; border-radius: 5px; color: #155724; }}
            .method {{ font-weight: bold; color: #007bff; }}
            .path {{ font-family: monospace; background: #e9ecef; padding: 2px 6px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 API de Red Neuronal de Emociones</h1>
            <div class="status">
                <strong>Estado del sistema:</strong> {status}
            </div>
            
            <h2>📋 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/predict</span><br>
                <strong>Función:</strong> Predice la emoción de un texto<br>
                <strong>Body:</strong> <code>{{"text": "Estoy muy feliz hoy"}}</code>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/feedback</span><br>
                <strong>Función:</strong> Lista todas las correcciones de feedback
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/feedback</span><br>
                <strong>Función:</strong> Envía una corrección de emoción<br>
                <strong>Body:</strong> <code>{{"text": "...", "predicted_emotion": "...", "corrected_emotion": "..."}}</code>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/feedback/{{id}}</span><br>
                <strong>Función:</strong> Obtiene un feedback específico por ID
            </div>
            
            <div class="endpoint">
                <span class="method">PUT</span> <span class="path">/feedback/{{id}}</span><br>
                <strong>Función:</strong> Actualiza una corrección existente
            </div>
            
            <div class="endpoint">
                <span class="method">DELETE</span> <span class="path">/feedback/{{id}}</span><br>
                <strong>Función:</strong> Elimina una corrección
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/train</span><br>
                <strong>Función:</strong> Reentrena el modelo con las correcciones acumuladas
            </div>
            
            <p><a href="/docs" target="_blank">📖 Ver documentación interactiva (Swagger)</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/predict", response_model=PredictionResponse)
async def predict_emotion(input_data: TextInput):
    if not services_available or not predictor:
        raise HTTPException(status_code=503, detail="Servicio de predicción no disponible")
    
    try:
        emotion, confidence = predictor.predecir(input_data.text)
        
        return PredictionResponse(
            emotion=emotion,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")

@app.get("/feedback", response_model=List[FeedbackItem])
async def get_feedback():
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    try:
        corrections = feedback_service.get_recent_feedback(limit=100)
        
        return [
            FeedbackItem(
                id=corr.get("id", 0),
                text=corr.get("text", ""),
                emotion=None,
                corrected_emotion=corr.get("correct_emotion", ""),
                user_id=corr.get("user_id", None),
                created_at=str(corr.get("created_at", "")) if corr.get("created_at") else None
            )
            for corr in corrections
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener feedback: {str(e)}")

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackInput, background_tasks: BackgroundTasks):
    if not services_available or not feedback_service or not predictor:
        raise HTTPException(status_code=503, detail="Servicios no disponibles")
    
    try:
        feedback_id = feedback_service.submit(feedback.text, feedback.corrected_emotion)
        
        background_tasks.add_task(retrain_model_background, epochs=2)
        
        return FeedbackResponse(
            message="Feedback registrado correctamente",
            id=feedback_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar feedback: {str(e)}")

@app.get("/feedback/{feedback_id}", response_model=FeedbackItem)
async def get_feedback_by_id(feedback_id: int):
    """
    Devuelve los datos de un feedback concreto
    """
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    try:
        correction = feedback_service.get_correction_by_id(feedback_id)
        
        if not correction:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        
        return FeedbackItem(
            id=correction.get("id"),
            text=correction.get("text"),
            emotion=correction.get("predicted_emotion"),
            corrected_emotion=correction.get("correct_emotion"),
            user_id=correction.get("user_id")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener feedback: {str(e)}")

@app.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: int, update_data: FeedbackUpdate):
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    try:
        success = feedback_service.update_correction(feedback_id, update_data.corrected_emotion)
        
        if not success:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        
        return {"message": "Feedback actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar feedback: {str(e)}")

@app.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int):
    if not services_available or not feedback_service:
        raise HTTPException(status_code=503, detail="Servicio de feedback no disponible")
    
    try:
        success = feedback_service.delete_correction(feedback_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Feedback no encontrado")
        
        return {"message": "Feedback eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar feedback: {str(e)}")

@app.post("/train", response_model=TrainResponse)
async def train_model(background_tasks: BackgroundTasks, epochs: int = 5, from_scratch: bool = False):
    if not services_available or not predictor:
        raise HTTPException(status_code=503, detail="Servicio de predicción no disponible")
    
    try:
        background_tasks.add_task(retrain_model_background, epochs, from_scratch)
        
        return TrainResponse(
            message="Entrenamiento iniciado en segundo plano",
            status="started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar entrenamiento: {str(e)}")

def retrain_model_background(epochs: int = 2, from_scratch: bool = False):
    try:
        print(f"🚀 Iniciando reentrenamiento (epochs={epochs}, from_scratch={from_scratch})")
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