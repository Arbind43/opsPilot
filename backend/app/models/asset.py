"""
OpsPilot — Asset Model
=======================
Hierarchical asset model (Plant → Area → Equipment → Component).
"""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Asset(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "assets"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    asset_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # plant | area | equipment | component
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="operational"
    )  # operational | degraded | failed | decommissioned
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Self-referential FK for asset hierarchy
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True
    )

    # Relationships
    parent = relationship("Asset", remote_side="Asset.id", back_populates="children")
    children = relationship("Asset", back_populates="parent", lazy="selectin")
    documents = relationship("Document", back_populates="asset", lazy="selectin")
    incidents = relationship("Incident", back_populates="asset", lazy="selectin")
    maintenance_records = relationship("MaintenanceRecord", back_populates="asset", lazy="selectin")
    inspections = relationship("Inspection", back_populates="asset", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Asset {self.name} ({self.asset_type})>"
