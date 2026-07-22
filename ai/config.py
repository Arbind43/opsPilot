"""
OpsPilot — AI Configuration
==============================
AI-specific settings for LLM, embedding, and pipeline parameters.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Walk up from this file (ai/config.py) to find the project-root .env
_HERE = Path(__file__).resolve()
_ENV_FILE = next(
    (str(p / ".env") for p in [_HERE.parent, _HERE.parents[1], _HERE.parents[2]]
     if (p / ".env").exists()),
    ".env",
)


class AISettings(BaseSettings):
    """AI-specific settings loaded from environment."""
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Providers ────────────────────────────────────
    LLM_PROVIDER: str = "gemini"  # "gemini" | "openai" | "groq"
    EMBEDDING_PROVIDER: str = "gemini"  # "gemini" | "openai" | "huggingface"

    # ── Google Gemini ─────────────────────────────────
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    # ── OpenAI ────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # ── HuggingFace (free local embeddings) ───────────
    HUGGINGFACE_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ── Groq ──────────────────────────────────────────
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ── Pipeline tuning ──────────────────────────────
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 2048
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MIN_CHUNK_SIZE: int = 100

    # ── Retrieval ─────────────────────────────────────
    VECTOR_SEARCH_TOP_K: int = 10
    GRAPH_SEARCH_DEPTH: int = 3
    RERANK_TOP_K: int = 5
    CONFIDENCE_THRESHOLD: float = 0.3

    # ── ChromaDB ──────────────────────────────────────
    DOCUMENTS_COLLECTION: str = "opspilot_documents"


ai_settings = AISettings()

# Convenience aliases for old imports
LLM_MODEL = (
    ai_settings.GEMINI_MODEL if ai_settings.LLM_PROVIDER == "gemini" else
    ai_settings.GROQ_MODEL if ai_settings.LLM_PROVIDER == "groq" else
    ai_settings.OPENAI_MODEL
)
LLM_TEMPERATURE = ai_settings.LLM_TEMPERATURE
LLM_MAX_TOKENS = ai_settings.LLM_MAX_TOKENS
EMBEDDING_MODEL = (
    ai_settings.GEMINI_EMBEDDING_MODEL if ai_settings.EMBEDDING_PROVIDER == "gemini" else
    ai_settings.HUGGINGFACE_EMBEDDING_MODEL if ai_settings.EMBEDDING_PROVIDER == "huggingface" else
    ai_settings.OPENAI_EMBEDDING_MODEL
)
EMBEDDING_DIMENSION = (
    384 if ai_settings.EMBEDDING_PROVIDER == "huggingface" else
    768 if ai_settings.EMBEDDING_PROVIDER == "gemini" else
    1536
)
CHUNK_SIZE = ai_settings.CHUNK_SIZE
CHUNK_OVERLAP = ai_settings.CHUNK_OVERLAP
MIN_CHUNK_SIZE = ai_settings.MIN_CHUNK_SIZE
VECTOR_SEARCH_TOP_K = ai_settings.VECTOR_SEARCH_TOP_K
GRAPH_SEARCH_DEPTH = ai_settings.GRAPH_SEARCH_DEPTH
RERANK_TOP_K = ai_settings.RERANK_TOP_K
CONFIDENCE_THRESHOLD = ai_settings.CONFIDENCE_THRESHOLD
DOCUMENTS_COLLECTION = ai_settings.DOCUMENTS_COLLECTION
