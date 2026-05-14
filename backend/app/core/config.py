"""Centralized application settings using pydantic-settings.

All configuration is loaded from environment variables.
Use `.env` file for local development and inject secrets via
env vars in production.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Application ──
    app_name: str = Field(default="SalesPredict AI CRM", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # ── Database ──
    database_url: str = Field(
        default="postgresql+asyncpg://salespredict:salespredict@localhost:5432/salespredict",
        alias="DATABASE_URL",
    )
    db_pool_size: int = Field(default=10, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, alias="DB_MAX_OVERFLOW")
    db_pool_pre_ping: bool = Field(default=True, alias="DB_POOL_PRE_PING")
    db_echo: bool = Field(default=False, alias="DB_ECHO")

    # ── Redis ──
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
    )
    redis_pool_size: int = Field(default=20, alias="REDIS_POOL_SIZE")

    # ── Qdrant ──
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_api_key: str | None = Field(default=None, alias="QDRANT_API_KEY")

    # ── Groq AI ──
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")

    # ── MLflow ──
    mlflow_tracking_uri: str = Field(
        default="http://localhost:5000",
        alias="MLFLOW_TRACKING_URI",
    )
    mlflow_experiment_name: str = Field(
        default="salespredict_forecast",
        alias="MLFLOW_EXPERIMENT_NAME",
    )

    # ── Security ──
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        alias="SECRET_KEY",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")

    # ── CORS ──
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        alias="CORS_ORIGINS",
    )

    # ── Celery ──
    celery_broker_url: str = Field(
        default="redis://localhost:6379/0",
        alias="CELERY_BROKER_URL",
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/0",
        alias="CELERY_RESULT_BACKEND",
    )
    celery_task_serializer: str = Field(default="json", alias="CELERY_TASK_SERIALIZER")
    celery_result_serializer: str = Field(
        default="json",
        alias="CELERY_RESULT_SERIALIZER",
    )
    celery_accept_content: list[str] = Field(
        default=["json"],
        alias="CELERY_ACCEPT_CONTENT",
    )
    celery_timezone: str = Field(default="UTC", alias="CELERY_TIMEZONE")
    celery_enable_utc: bool = Field(default=True, alias="CELERY_ENABLE_UTC")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, str):
            import json

            return json.loads(v)
        return v

    @field_validator("celery_accept_content", mode="before")
    @classmethod
    def assemble_accept_content(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [item.strip() for item in v.split(",")]
        if isinstance(v, str):
            import json

            return json.loads(v)
        return v


settings = Settings()
