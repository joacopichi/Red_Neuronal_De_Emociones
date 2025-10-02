from src.services.feedback_service import FeedbackService

def test_feedback_service_submit_and_dataset():
    service = FeedbackService()
    feedback_id = service.submit("Estoy triste", "tristeza")
    assert isinstance(feedback_id, int)

    dataset = service.dataset()
    assert isinstance(dataset, list)
    assert all(isinstance(item, tuple) for item in dataset)