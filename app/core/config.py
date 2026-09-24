from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Pandac POS API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    api_v1_str: str = Field(default="/v1")

    # Database
    database_url: str = Field(default="postgresql://user:password@localhost:5432/pandac_pos")
    database_url_test: Optional[str] = Field(default=None)

    # Security
    secret_key: str = Field(default="changeme-secret-key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # CORS
    backend_cors_origins: List[str] = Field(default_factory=list)

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/0")
    celery_result_backend: str = Field(default="redis://localhost:6379/0")

    # Email (optional)
    smtp_tls: bool = Field(default=True)
    smtp_port: int = Field(default=587)
    smtp_host: Optional[str] = Field(default=None)
    smtp_user: Optional[str] = Field(default=None)
    smtp_password: Optional[str] = Field(default=None)

    # Logging
    log_level: str = Field(default="INFO")


settings = Settings()