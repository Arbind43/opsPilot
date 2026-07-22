"""
OpsPilot — Maintenance Record Model
=====================================
"""

from typing import Optional
import uuid
from datetime import datetime
from pydantic import Field
from app.models.base import BaseDocument


class MaintenanceRecord(BaseDocument):
    title: str = Field(index=True)
    description: Optional[str] = None
    maintenance_type: str  # preventive | corrective | predictive
    status: str = "scheduled"  # scheduled | in_progress | completed | cancelled
    cost: Optional[float] = None

    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    asset_id: uuid.UUID
    performed_by: Optional[uuid.UUID] = None

    class Settings:
        name = "maintenance_records"

    def __repr__(self) -> str:
        return f"<MaintenanceRecord {self.title} ({self.maintenance_type})>"
