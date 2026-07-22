"""
OpsPilot — Conversation & Message Models
==========================================
Stores AI Copilot conversation history for memory and auditability.
"""

from typing import Optional, Dict, Any
import uuid
from pydantic import Field
from app.models.base import BaseDocument


class Conversation(BaseDocument):
    title: str = "New Conversation"
    user_id: uuid.UUID = Field(index=True)

    class Settings:
        name = "conversations"

    def __repr__(self) -> str:
        return f"<Conversation {self.title}>"


class Message(BaseDocument):
    conversation_id: uuid.UUID = Field(index=True)
    role: str  # user | assistant
    content: str
    citations: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    metadata_json: Optional[Dict[str, Any]] = None

    class Settings:
        name = "messages"

    def __repr__(self) -> str:
        return f"<Message {self.role} in {self.conversation_id}>"
