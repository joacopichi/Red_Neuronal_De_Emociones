from src.services.feedback_service import FeedbackService

def test_feedback_service_add_feedback():
    service = FeedbackService()
    feedback = service.save_feedback("Estoy triste", "tristeza")
    assert feedback is not None