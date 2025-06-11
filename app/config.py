from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "URL Shortener"
    DATABASE_URL: str
    SECRET_KEY: str
    BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

