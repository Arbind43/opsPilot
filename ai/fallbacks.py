"""
OpsPilot — Local fallback implementations
=======================================
Provides lightweight demo-mode fallbacks when external AI services or
vector stores are not configured.
"""

import hashlib
import logging
import re
from typing import Any, List
from types import SimpleNamespace

logger = logging.getLogger(__name__)


class FallbackLLM:
    """Simple local LLM fallback for demo mode."""

    def __init__(self, provider: str = "local", temperature: float = 0.0):
        self.provider = provider
        self.temperature = temperature

    async def ainvoke(self, value: Any, config: Any = None, **kwargs) -> Any:
        content = self._format_response(value)
        return SimpleNamespace(content=content)

    async def astream(self, value: Any, config: Any = None, **kwargs):
        content = self._format_response(value)
        yield SimpleNamespace(content=content)

    def with_structured_output(self, schema: Any):
        return StructuredFallbackLLM(schema=schema, parent=self)

    def _format_response(self, value: Any) -> str:
        if isinstance(value, dict):
            context = value.get("context", "")
            question = value.get("question", "")
            if context and question:
                return (
                    f"Demo response for: {question}\n\n"
                    f"Context summary: {context[:240]}"
                )
            if question:
                return f"Demo response for: {question}"
            return str(value)
        return str(value)


class StructuredFallbackLLM:
    """Structured-output wrapper for the local fallback LLM."""

    def __init__(self, schema: Any, parent: FallbackLLM):
        self.schema = schema
        self.parent = parent

    async def ainvoke(self, value: Any, config: Any = None, **kwargs) -> Any:
        payload = {
            "document_type": "Operations Manual",
            "reason": "This is a demo fallback response because no live AI provider is configured.",
            "priority": "medium",
        }
        if self.schema is not None:
            try:
                return self.schema.model_validate(payload)
            except Exception:
                return payload
        return payload


class FallbackEmbeddings:
    """Deterministic local embedding fallback."""

    def __init__(self, dimensions: int = 32):
        self.dimensions = dimensions

    async def aembed_query(self, text: str) -> List[float]:
        return self._embed_text(text)

    async def aembed_documents(self, documents: List[str]) -> List[List[float]]:
        return [self._embed_text(doc) for doc in documents]

    def _embed_text(self, text: str) -> List[float]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        if not tokens:
            return [0.0] * self.dimensions

        vector = [0.0] * self.dimensions
        seen = set()
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:2], "big") % self.dimensions
            value = (int.from_bytes(digest[2:4], "big") / 65535.0) + 0.05
            vector[bucket] += value

        norm = sum(v * v for v in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]


class LocalVectorStore:
    """In-memory vector store used when Pinecone is unavailable."""

    def __init__(self):
        self._vectors: List[dict] = []

    def clear(self) -> None:
        self._vectors.clear()

    def get_index(self):
        return self

    def upsert(self, vectors: List[dict]) -> None:
        for incoming in vectors:
            existing = next((item for item in self._vectors if item.get("id") == incoming.get("id")), None)
            if existing is not None:
                self._vectors.remove(existing)
            self._vectors.append(incoming)

    def query(self, vector: List[float], top_k: int = 5, include_metadata: bool = True):
        results = []
        for item in self._vectors:
            values = item.get("values") or []
            score = self._cosine_similarity(vector, values)
            results.append(SimpleNamespace(metadata=item.get("metadata", {}), score=score, id=item.get("id")))

        results.sort(key=lambda entry: entry.score, reverse=True)
        return SimpleNamespace(matches=results[:top_k])

    def _cosine_similarity(self, left: List[float], right: List[float]) -> float:
        if not left or not right:
            return 0.0
        left_len = len(left)
        right_len = len(right)
        if left_len != right_len:
            right = right[:left_len] + [0.0] * max(0, left_len - right_len)
        dot = sum(a * b for a, b in zip(left, right))
        norm_left = sum(a * a for a in left) ** 0.5 or 1.0
        norm_right = sum(b * b for b in right) ** 0.5 or 1.0
        return dot / (norm_left * norm_right)


local_vector_store = LocalVectorStore()
