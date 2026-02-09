"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Kumo", description="Application name")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Runtime environment"
    )
    debug: bool = Field(default=False, description="Enable debug mode")

    # Database (async)
    db_url: PostgresDsn = Field(
        default="postgresql+asyncpg://kumo:kumo@localhost:5432/kumo",
        description="PostgreSQL connection URL (asyncpg driver)",
    )

    # Redis
    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for cache and Celery broker",
    )

    # Celery (default to redis_url when not set)
    celery_broker_url: str | None = Field(
        default=None,
        description="Celery broker URL (defaults to redis_url if not set)",
    )
    celery_result_backend: str | None = Field(
        default=None,
        description="Celery result backend (defaults to redis_url if not set)",
    )

    @property
    def celery_broker(self) -> str:
        """Celery broker URL (uses redis_url if not set)."""
        return self.celery_broker_url or str(self.redis_url)

    @property
    def celery_result(self) -> str:
        """Celery result backend URL (uses redis_url if not set)."""
        return self.celery_result_backend or str(self.redis_url)

    @property
    def sync_db_url(self) -> str:
        """Synchronous DB URL for Alembic/migrations (postgresql://)."""
        return str(self.db_url).replace("postgresql+asyncpg://", "postgresql://")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
