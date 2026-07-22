"""
OpsPilot — LLM Factory
========================
Central factory for getting the configured LLM and embedding model.
Supports Google Gemini and OpenAI. Switch via LLM_PROVIDER in .env.
"""

import logging
from functools import lru_cache
from typing import Any

from ai.fallbacks import FallbackEmbeddings, FallbackLLM

logger = logging.getLogger(__name__)


def get_llm(provider: str = None, temperature: float = 0.0, model_name: str = None) -> Any:
    """
    Returns a LangChain-compatible LLM instance.
    provider: 'gemini' | 'openai' | 'groq' | None (auto from settings)
    """
    if provider is None:
        from ai.config import ai_settings
        provider = ai_settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        try:
            return _get_gemini_llm(temperature, model_name)
        except Exception as exc:
            logger.warning("Falling back to local LLM: %s", exc)
            return FallbackLLM(provider="gemini", temperature=temperature)
    elif provider == "openai":
        try:
            return _get_openai_llm(temperature)
        except Exception as exc:
            logger.warning("Falling back to local LLM: %s", exc)
            return FallbackLLM(provider="openai", temperature=temperature)
    elif provider == "groq":
        try:
            return _get_groq_llm(temperature, model_name)
        except Exception as exc:
            logger.warning("Falling back to local LLM: %s", exc)
            return FallbackLLM(provider="groq", temperature=temperature)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def _get_gemini_llm(temperature: float = 0.0, model_name: str = None):
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from ai.config import ai_settings
        if not ai_settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in .env")
        return ChatGoogleGenerativeAI(
            model=model_name or ai_settings.GEMINI_MODEL,
            google_api_key=ai_settings.GOOGLE_API_KEY,
            temperature=temperature,
            convert_system_message_to_human=True,
        )
    except ImportError:
        logger.error("langchain-google-genai not installed. Run: pip install langchain-google-genai")
        raise


def _get_openai_llm(temperature: float = 0.0):
    try:
        from langchain_openai import ChatOpenAI
        from ai.config import ai_settings
        if not ai_settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in .env")
        return ChatOpenAI(
            model=ai_settings.OPENAI_MODEL,
            api_key=ai_settings.OPENAI_API_KEY,
            temperature=temperature,
        )
    except ImportError:
        logger.error("langchain-openai not installed. Run: pip install langchain-openai")
        raise


def _get_groq_llm(temperature: float = 0.0, model_name: str = None):
    try:
        from langchain_groq import ChatGroq
        from ai.config import ai_settings
        if not ai_settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in .env")
        return ChatGroq(
            model_name=model_name or ai_settings.GROQ_MODEL,
            groq_api_key=ai_settings.GROQ_API_KEY,
            temperature=temperature,
        )
    except ImportError:
        logger.error("langchain-groq not installed. Run: pip install langchain-groq")
        raise


def get_embedding_model(provider: str = None):
    """Returns a LangChain-compatible embedding model."""
    if provider is None:
        from ai.config import ai_settings
        provider = ai_settings.EMBEDDING_PROVIDER.lower()

    if provider == "gemini":
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            from ai.config import ai_settings
            if not ai_settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is not set in .env")
            return GoogleGenerativeAIEmbeddings(
                model=ai_settings.GEMINI_EMBEDDING_MODEL,
                google_api_key=ai_settings.GOOGLE_API_KEY,
            )
        except Exception as exc:
            logger.warning("Falling back to local embeddings: %s", exc)
            return FallbackEmbeddings()
    elif provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
            from ai.config import ai_settings
            if not ai_settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set in .env")
            return OpenAIEmbeddings(
                model=ai_settings.OPENAI_EMBEDDING_MODEL,
                api_key=ai_settings.OPENAI_API_KEY,
            )
        except Exception as exc:
            logger.warning("Falling back to local embeddings: %s", exc)
            return FallbackEmbeddings()
    elif provider == "huggingface":
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from ai.config import ai_settings
            return HuggingFaceEmbeddings(
                model_name=ai_settings.HUGGINGFACE_EMBEDDING_MODEL
            )
        except Exception as exc:
            logger.warning("Falling back to local embeddings: %s", exc)
            return FallbackEmbeddings()
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
