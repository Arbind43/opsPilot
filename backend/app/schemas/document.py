"""
OpsPilot — Document Schemas
==============================
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    file_type: str
    doc_category: str | None
    file_size: int
    processing_status: str
    processing_error: str | None
    version: int
    uploaded_by: UUID
    asset_id: UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentStatusResponse(BaseModel):
    id: UUID
    processing_status: str
    processing_error: str | None
