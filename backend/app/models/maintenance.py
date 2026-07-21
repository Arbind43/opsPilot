"""
OpsPilot — Maintenance Record Model
=====================================
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class MaintenanceRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "maintenance_records"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    maintenance_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # preventive | corrective | predictive
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="scheduled"
    )  # scheduled | in_progress | completed | cancelled
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)

    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Foreign keys
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False
    )
    performed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_records")
    performer = relationship("User", foreign_keys=[performed_by])

    def __repr__(self) -> str:
        return f"<MaintenanceRecord {self.title} ({self.maintenance_type})>"
