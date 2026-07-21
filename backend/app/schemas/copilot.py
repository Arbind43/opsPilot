"""
OpsPilot — Copilot Schemas
=============================
Schemas for AI Copilot conversations and queries.
"""

from datetime import datetime
from typing import Any, List
from uuid import UUID

from pydantic import BaseModel, Field


class CopilotQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    conversation_id: UUID | None = None
    context_filters: dict[str, Any] | None = None  # Optional filters (asset_id, doc_type, etc.)


class Citation(BaseModel):
    document_id: UUID
    document_title: str
    chunk_content: str
    relevance_score: float
    page_number: int | None = None


class CopilotResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    confidence_score: float
    conversation_id: UUID
    metadata: dict[str, Any] | None = None


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    citations: dict | None = None
    confidence_score: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
