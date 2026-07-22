"""
OpsPilot — Application Configuration
=====================================
Centralized settings using Pydantic Settings.
All values are loaded from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import List

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
    # Comma-separated list of allowed origins, e.g.:
    # "https://myapp.onrender.com,http://localhost:5173"
    # Using str (not List[str]) avoids pydantic-settings JSON-parse errors
    # when Render injects the value as a plain environment variable string.
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    def get_cors_origins(self) -> List[str]:
        """Return CORS_ORIGINS as a list — handles comma-separated or JSON array strings."""
        raw = self.CORS_ORIGINS.strip()
        if raw.startswith("["):
            import json
            try:
                return json.loads(raw)
            except Exception:
                pass
        return [o.strip().strip('"').strip("'") for o in raw.split(",") if o.strip()]

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
