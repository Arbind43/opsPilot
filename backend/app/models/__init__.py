"""
OpsPilot — SQLAlchemy Models Package
=====================================
All ORM model classes are imported here for Alembic auto-detection.
"""

from app.models.base import BaseDocument
from app.models.user import User
from app.models.asset import Asset
from app.models.document import Document, DocumentChunk
from app.models.incident import Incident
from app.models.maintenance import MaintenanceRecord
from app.models.inspection import Inspection
from app.models.report import Report
from app.models.conversation import Conversation, Message
from app.models.audit_log import AuditLog

__all__ = [
    "BaseDocument",
    "User",
    "Asset",
    "Document",
    "DocumentChunk",
    "Incident",
    "MaintenanceRecord",
    "Inspection",
    "Report",
    "Conversation",
    "Message",
    "AuditLog",
]
