"""
OpsPilot — Report Model
=========================
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Report(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reports"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # rca | compliance | maintenance | summary
    content: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft"
    )  # draft | generated | approved

    # Foreign keys
    generated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True
    )

    # Relationships
    generator = relationship("User", foreign_keys=[generated_by])
    asset = relationship("Asset", foreign_keys=[asset_id])

    def __repr__(self) -> str:
        return f"<Report {self.title} ({self.report_type})>"
