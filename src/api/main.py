from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import root, prediction, feedback, training, health

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

app.include_router(root.router, tags=["UI"])
app.include_router(prediction.router, tags=["Prediction"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(training.router, prefix="/train", tags=["Training"])
app.include_router(health.router, prefix="/health", tags=["Health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
