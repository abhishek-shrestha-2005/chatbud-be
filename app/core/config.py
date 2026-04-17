# app/core/config.py — should look like this
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    DATABASE_URL: str = ""
    FIREBASE_SERVICE_ACCOUNT_PATH: str = (
        "chatembed-91c26-firebase-adminsdk-fbsvc-6038d72c11.json"
    )
    GEMINI_API_KEY: str = ""


settings = Settings()
