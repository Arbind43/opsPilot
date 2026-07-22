"""
OpsPilot — Report Model
=========================
"""

from typing import Optional, Dict, Any
import uuid
from pydantic import Field
from app.models.base import BaseDocument


class Report(BaseDocument):
    title: str = Field(index=True)
    report_type: str  # rca | compliance | maintenance | summary
    content: Optional[Dict[str, Any]] = None
    status: str = "draft"  # draft | generated | approved

    generated_by: uuid.UUID
    asset_id: Optional[uuid.UUID] = None

    class Settings:
        name = "reports"

    def __repr__(self) -> str:
        return f"<Report {self.title} ({self.report_type})>"
