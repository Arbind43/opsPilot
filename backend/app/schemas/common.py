"""
OpsPilot — Common Schemas
===========================
Shared Pydantic models: pagination, status, enums.
"""

from enum import Enum
from typing import Generic, List, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────

class UserRole(str, Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    OPERATOR = "operator"
    VIEWER = "viewer"


class AssetType(str, Enum):
    PLANT = "plant"
    AREA = "area"
    EQUIPMENT = "equipment"
    COMPONENT = "component"


class AssetStatus(str, Enum):
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    FAILED = "failed"
    DECOMMISSIONED = "decommissioned"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocCategory(str, Enum):
    SOP = "sop"
    MANUAL = "manual"
    DRAWING = "drawing"
    LOG = "log"
    REGULATION = "regulation"
    REPORT = "report"


# ── Pagination ───────────────────────────────────────

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


# ── Common Responses ─────────────────────────────────

class StatusMessage(BaseModel):
    status: str = "ok"
    message: str = ""


class IDResponse(BaseModel):
    id: UUID
