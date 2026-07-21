"""
OpsPilot — Asset Schemas
==========================
"""

from datetime import datetime
from typing import Any, List
from uuid import UUID

from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    asset_type: str = Field(..., pattern="^(plant|area|equipment|component)$")
    serial_number: str | None = None
    location: str | None = None
    status: str = "operational"
    description: str | None = None
    metadata_json: dict | None = None
    parent_id: UUID | None = None


class AssetUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    location: str | None = None
    description: str | None = None
    metadata_json: dict | None = None


class AssetResponse(BaseModel):
    id: UUID
    name: str
    asset_type: str
    serial_number: str | None
    location: str | None
    status: str
    description: str | None
    metadata_json: dict | None
    parent_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssetTreeNode(BaseModel):
    id: UUID
    name: str
    asset_type: str
    status: str
    children: List["AssetTreeNode"] = []

    model_config = {"from_attributes": True}


class TimelineEvent(BaseModel):
    id: UUID
    event_type: str  # incident | maintenance | inspection | document
    title: str
    description: str | None = None
    timestamp: datetime
    metadata: dict[str, Any] | None = None
