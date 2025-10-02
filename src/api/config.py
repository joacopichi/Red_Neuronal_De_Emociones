from pydantic import BaseSettings


class APISettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    DATABASE_URL: str = "sqlite:///./red_emociones.db"

    MODEL_PATH: str = "modelo.keras"

    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"


settings = APISettings()
