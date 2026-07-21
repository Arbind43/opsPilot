"""
OpsPilot — Incident Schemas
==============================
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    severity: str = Field("medium", pattern="^(critical|high|medium|low)$")
    asset_id: UUID
    occurred_at: datetime | None = None


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: str | None = None
    status: str | None = None
    root_cause: dict | None = None
    resolved_at: datetime | None = None


class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    severity: str
    status: str
    root_cause: dict | None
    asset_id: UUID
    reported_by: UUID
    occurred_at: datetime | None
    resolved_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
