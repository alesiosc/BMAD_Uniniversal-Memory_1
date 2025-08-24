# apps/api/src/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    GOOGLE_API_KEY: str  # Add this line

    class Config:
        env_file = ".env"

settings = Settings()