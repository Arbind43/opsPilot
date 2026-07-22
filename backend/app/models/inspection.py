"""
OpsPilot — Inspection Model
==============================
"""

from typing import Optional, Dict, Any
import uuid
from datetime import date
from pydantic import Field
from app.models.base import BaseDocument


class Inspection(BaseDocument):
    title: str = Field(index=True)
    findings: Optional[str] = None
    result: str = "pass"  # pass | fail | conditional
    inspection_date: date
    next_due_date: Optional[date] = None
    checklist_results: Optional[Dict[str, Any]] = None

    asset_id: uuid.UUID
    inspector_id: uuid.UUID

    class Settings:
        name = "inspections"

    def __repr__(self) -> str:
        return f"<Inspection {self.title} ({self.result})>"
