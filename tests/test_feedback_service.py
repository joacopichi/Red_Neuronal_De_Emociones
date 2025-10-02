from src.services.feedback_service import FeedbackService

def test_feedback_service_add_feedback():
    service = FeedbackService()
    feedback = service.add_feedback("Estoy triste", "tristeza")
    assert feedback is not None
    assert "frase" in feedback or "sentence" in feedback