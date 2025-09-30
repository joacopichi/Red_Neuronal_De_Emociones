from fastapi import APIRouter, BackgroundTasks, HTTPException
from api.schemas import TextInput, PredictionResponse
from services.predictor_service import PredictorService
from services.feedback_service import FeedbackService
from api.utils import retrain_model_background

router = APIRouter()

predictor = PredictorService()
feedback_service = FeedbackService()

@router.post("/predict_feedback", response_model=PredictionResponse)
async def predict_feedback(
    input_data: TextInput,
    background_tasks: BackgroundTasks,
    corrected_emotion: str | None = None
):
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
