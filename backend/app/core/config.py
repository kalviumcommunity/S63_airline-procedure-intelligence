"""Application Configuration using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for SkyOps Intelligence backend."""

    # Project Information
    PROJECT_NAME: str = "SkyOps Intelligence Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API Routing
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # LLM Settings
    LLM_PROVIDER: str = Field(
        default="mock", description="LLM provider: 'mock', 'openai', or 'anthropic'"
    )
    OPENAI_API_KEY: str | None = Field(default=None)
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    ANTHROPIC_API_KEY: str | None = Field(default=None)
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-large"
    LLM_TEMPERATURE: float = 0.0
    LLM_REQUEST_TIMEOUT_SECONDS: float = 30.0
    LLM_MAX_RETRIES: int = 2

    # Vector & Relational Storage
    VECTOR_DB_TYPE: str = "qdrant"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str | None = None
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
