from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Anthropic
    ANTHROPIC_API_KEY: str

    # NYC Open Data
    NYC_OPEN_DATA_APP_TOKEN: str
    NYC_311_ENDPOINT: str
    NYC_DOT_CAMERA_API_URL: str

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173"

    # App
    APP_ENV: str = "development"
    CASCADE_PLAYBACK_SPEED: float = 1.0
    CV_POLL_INTERVAL: int = 30

    # Feature flags
    ENABLE_CV: bool = True
    ENABLE_TGNN: bool = True

    # ML paths — only validated when their feature flag is true
    MODEL_CHECKPOINT_PATH: Optional[str] = None
    YOLO_MODEL_PATH: Optional[str] = None

    @model_validator(mode="after")
    def validate_ml_paths(self) -> "Settings":
        if self.ENABLE_TGNN and not self.MODEL_CHECKPOINT_PATH:
            raise ValueError("MODEL_CHECKPOINT_PATH is required when ENABLE_TGNN=true")
        if self.ENABLE_CV and not self.YOLO_MODEL_PATH:
            raise ValueError("YOLO_MODEL_PATH is required when ENABLE_CV=true")
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
