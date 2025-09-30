from fastapi import APIRouter, BackgroundTasks, HTTPException
from api.schemas import TrainResponse
from api.utils import retrain_model_background
from services.predictor_service import PredictorService

router = APIRouter()
predictor = PredictorService()

@router.post("/", response_model=TrainResponse)
async def train_model(background_tasks: BackgroundTasks, epochs: int = 50, from_scratch: bool = False):
    if not predictor:
        raise HTTPException(status_code=503, detail="Servicio de predicción no disponible")
    background_tasks.add_task(retrain_model_background, epochs=epochs, from_scratch=from_scratch)
    return TrainResponse(message="Entrenamiento en segundo plano iniciado", status="started")
