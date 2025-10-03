"""
Application settings for Qwen API Service Template.

Uses Pydantic settings for configuration management with support for:
- Environment variables
- .env files
- Type validation
- Default values
"""

import secrets
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, field_validator, ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    """

    # Project Information
    PROJECT_NAME: str = "Qwen API Service Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A modern API service template with Qwen AI integration patterns"
    API_V1_PREFIX: str = "/api/v1"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # React default
        "http://127.0.0.1:3000",
        "http://localhost:8080",  # Vue default
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """Parse CORS origins from environment variable."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/qwen_api"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30

    # Redis (for caching and rate limiting)
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # 5 minutes

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Qwen AI Integration
    QWEN_API_BASE_URL: str = "https://api.qwen.com/v1"
    QWEN_API_KEY: Optional[str] = None
    QWEN_MODEL: str = "qwen-turbo"
    QWEN_MAX_TOKENS: int = 2048
    QWEN_TEMPERATURE: float = 0.7

    # External APIs
    SENTRY_DSN: Optional[str] = None

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".txt"]

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment setting."""
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v

    @field_validator("DEBUG")
    @classmethod
    def validate_debug_with_environment(cls, v: bool, info: ValidationInfo) -> bool:
        """Debug should be False in production."""
        if info.data and info.data.get("ENVIRONMENT") == "production" and v:
            raise ValueError("Debug mode cannot be enabled in production")
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()