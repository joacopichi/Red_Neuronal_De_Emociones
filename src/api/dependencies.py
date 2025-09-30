from services.predictor_service import PredictorService
from services.feedback_service import FeedbackService

try:
    predictor = PredictorService()
    feedback_service = FeedbackService()
    services_available = True
except Exception as e:
    print(f"❌ Error inicializando servicios: {e}")
    predictor = None
    feedback_service = None
    services_available = False
