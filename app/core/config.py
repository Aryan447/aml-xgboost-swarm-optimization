import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AML Detection System"
    API_V1_STR: str = "/api/v1"

    # Paths (Defaults work for Docker, can be overridden by env vars)
    MODEL_DIR: str = os.getenv("MODEL_DIR", "/app/models")

    class Config:
        case_sensitive = True

settings = Settings()
