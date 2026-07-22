"""
OpsPilot — Audit Log Model
=============================
Tracks all significant user actions for security and compliance.
"""

from typing import Optional, Dict, Any
import uuid
from pydantic import Field
from app.models.base import BaseDocument


class AuditLog(BaseDocument):
    user_id: uuid.UUID = Field(index=True)
    action: str = Field(index=True)
    resource_type: str
    resource_id: Optional[uuid.UUID] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None

    class Settings:
        name = "audit_logs"

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} on {self.resource_type}>"
