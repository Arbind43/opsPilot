"""
OpsPilot — LLM Factory
========================
Central factory for getting the configured LLM and embedding model.
Supports Google Gemini and OpenAI. Switch via LLM_PROVIDER in .env.
"""

import logging
from functools import lru_cache
from typing import Any

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
        return _get_gemini_llm(temperature, model_name)
    elif provider == "openai":
        return _get_openai_llm(temperature)
    elif provider == "groq":
        return _get_groq_llm(temperature, model_name)
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
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from ai.config import ai_settings
        return GoogleGenerativeAIEmbeddings(
            model=ai_settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=ai_settings.GOOGLE_API_KEY,
        )
    elif provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        from ai.config import ai_settings
        return OpenAIEmbeddings(
            model=ai_settings.OPENAI_EMBEDDING_MODEL,
            api_key=ai_settings.OPENAI_API_KEY,
        )
    elif provider == "huggingface":
        # Use ChromaDB's built-in ONNX MiniLM embedder — zero extra dependencies needed
        # It's already installed as part of chromadb package
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
        onnx_ef = ONNXMiniLM_L6_V2()

        class ChromaEmbeddingWrapper:
            """Wraps ChromaDB's ONNX embedder to be LangChain-compatible."""
            def embed_documents(self, texts):
                return onnx_ef(texts)
            def embed_query(self, text):
                return onnx_ef([text])[0]
            async def aembed_query(self, text):
                return self.embed_query(text)
            async def aembed_documents(self, texts):
                return self.embed_documents(texts)

        return ChromaEmbeddingWrapper()
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
