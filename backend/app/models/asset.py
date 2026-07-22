"""
OpsPilot — Asset Model
=======================
Hierarchical asset model (Plant → Area → Equipment → Component).
"""

from typing import Optional, Dict, Any
import uuid
from pydantic import Field
from app.models.base import BaseDocument

class Asset(BaseDocument):
    name: str = Field(index=True)
    asset_type: str  # plant | area | equipment | component
    serial_number: Optional[str] = Field(default=None, unique=True)
    location: Optional[str] = None
    status: str = "operational"  # operational | degraded | failed | decommissioned
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

    parent_id: Optional[uuid.UUID] = None

    class Settings:
        name = "assets"

    def __repr__(self) -> str:
        return f"<Asset {self.name} ({self.asset_type})>"
