"""
OpsPilot — Report Schemas
============================
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    report_type: str = Field(..., pattern="^(rca|compliance|maintenance|summary)$")
    asset_id: UUID | None = None


class ReportResponse(BaseModel):
    id: UUID
    title: str
    report_type: str
    content: dict | None
    status: str
    generated_by: UUID
    asset_id: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}
