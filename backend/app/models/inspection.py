"""
OpsPilot — Inspection Model
==============================
"""

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Inspection(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inspections"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    findings: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pass"
    )  # pass | fail | conditional
    inspection_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    checklist_results: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Foreign keys
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False
    )
    inspector_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # Relationships
    asset = relationship("Asset", back_populates="inspections")
    inspector = relationship("User", foreign_keys=[inspector_id])

    def __repr__(self) -> str:
        return f"<Inspection {self.title} ({self.result})>"
