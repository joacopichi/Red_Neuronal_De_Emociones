from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas import FeedbackItem, FeedbackUpdate
from services.feedback_service import FeedbackService
from services.predictor_service import PredictorService

router = APIRouter()
feedback_service = FeedbackService()
predictor_service = PredictorService()


@router.get("/", response_model=List[FeedbackItem])
async def get_feedback():
    corrections = feedback_service.get_recent_feedback(limit=100)
    result = []

    for corr in corrections:
        pred, _ = (
            predictor_service.predecir(corr["text"]) if corr.get("text") else ("", 0.0)
        )

        result.append(
            FeedbackItem(
                id=corr.get("id", 0),
                text=corr.get("text", ""),
                predicted_emotion=pred,
                corrected_emotion=corr.get("correct_emotion", ""),
                created_at=(
                    str(corr.get("created_at")) if corr.get("created_at") else None
                ),
            )
        )
    return result


@router.put("/{feedback_id}", response_model=FeedbackItem)
async def update_feedback(feedback_id: int, update_data: FeedbackUpdate):
    success = feedback_service.update_correction(
        feedback_id, update_data.corrected_emotion
    )
    if not success:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")

    updated = feedback_service.get_correction_by_id(feedback_id)
    pred, _ = predictor_service.predecir(updated["text"]) if updated else ("", 0.0)

    return FeedbackItem(
        id=updated.get("id", 0),
        text=updated.get("text", ""),
        predicted_emotion=pred,
        corrected_emotion=updated.get("correct_emotion", ""),
        created_at=(
            str(updated.get("created_at")) if updated.get("created_at") else None
        ),
    )


@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: int):
    success = feedback_service.delete_correction(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    return {"message": "Feedback eliminado correctamente"}
