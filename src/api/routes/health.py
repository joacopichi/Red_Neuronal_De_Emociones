from fastapi import APIRouter
from services.predictor_service import PredictorService
from services.feedback_service import FeedbackService
from db.database import db_singleton

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "services": {
            "predictor": PredictorService() is not None,
            "feedback": FeedbackService() is not None,
            "database": db_singleton is not None,
        },
        "version": "1.0.0",
    }
