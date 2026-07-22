"""
OpsPilot — Application Configuration
=====================================
Centralized settings using Pydantic Settings.
All values are loaded from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import Any, List

from pydantic import field_validator

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate the .env file: it lives at the project root (opspilot/),
# which is two directories above this config.py (backend/app/config.py).
_HERE = Path(__file__).resolve()
_ENV_FILE = next(
    (str(p / ".env") for p in [_HERE.parents[1], _HERE.parents[2], _HERE.parents[3]]
     if (p / ".env").exists()),
    ".env",  # fallback — let pydantic-settings handle the missing file
)


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── General ──────────────────────────────────────
    APP_NAME: str = "OpsPilot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # ── Server ───────────────────────────────────────
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Accept JSON array, comma-separated string, or list from env vars."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            # JSON array: '["a","b"]'
            if v.startswith("["):
                import json
                return json.loads(v)
            # Comma-separated: 'http://a.com,http://b.com'
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # ── Auth / JWT ───────────────────────────────────
    SECRET_KEY: str = "change-me-to-a-random-64-char-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── MongoDB ──────────────────────────────────────
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "opspilot"

    # ── Neo4j ────────────────────────────────────────
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j_secret"

    # ── Pinecone ─────────────────────────────────────
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = "opspilot"

    # ── Redis ────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── LLM ──────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_EMBEDDING_MODEL: str = "models/text-embedding-004"

    LLM_PROVIDER: str = "gemini"  # "openai", "gemini", or "groq"
    EMBEDDING_PROVIDER: str = "gemini"  # "openai" or "gemini"

    # ── Groq ─────────────────────────────────────────
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ── File Storage ─────────────────────────────────
    UPLOAD_DIR: str = "./storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50


@lru_cache()
def get_settings() -> Settings:
    """Singleton settings instance (cached)."""
    return Settings()
