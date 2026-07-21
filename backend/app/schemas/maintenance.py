"""
OpsPilot — Maintenance Schemas
=================================
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MaintenanceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    maintenance_type: str = Field(..., pattern="^(preventive|corrective|predictive)$")
    asset_id: UUID
    scheduled_at: datetime | None = None
    cost: float | None = None


class MaintenanceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    cost: float | None = None
    completed_at: datetime | None = None


class MaintenanceResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    maintenance_type: str
    status: str
    cost: float | None
    asset_id: UUID
    performed_by: UUID | None
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
