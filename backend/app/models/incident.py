"""
OpsPilot — Incident Model
===========================
"""

from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from pydantic import Field
from app.models.base import BaseDocument


class Incident(BaseDocument):
    title: str = Field(index=True)
    description: Optional[str] = None
    severity: str = "medium"  # critical | high | medium | low
    status: str = "open"  # open | investigating | resolved | closed
    root_cause: Optional[Dict[str, Any]] = None

    occurred_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    asset_id: uuid.UUID
    reported_by: uuid.UUID

    class Settings:
        name = "incidents"

    def __repr__(self) -> str:
        return f"<Incident {self.title} ({self.severity}/{self.status})>"
