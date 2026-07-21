"""
OpsPilot — Inspection Schemas
================================
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class InspectionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    findings: str | None = None
    result: str = Field("pass", pattern="^(pass|fail|conditional)$")
    inspection_date: date
    next_due_date: date | None = None
    asset_id: UUID
    checklist_results: dict | None = None


class InspectionResponse(BaseModel):
    id: UUID
    title: str
    findings: str | None
    result: str
    inspection_date: date
    next_due_date: date | None
    asset_id: UUID
    inspector_id: UUID
    checklist_results: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}
