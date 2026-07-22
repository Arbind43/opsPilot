"""
OpsPilot — Settings and Audit Log Service
===========================================
Uses Beanie ODM for MongoDB operations.
"""

from typing import List

from app.models.audit_log import AuditLog


class SettingsService:
    """No session needed — Beanie operates directly on documents."""

    async def get_audit_logs(self, offset: int = 0, limit: int = 100) -> List[AuditLog]:
        return (
            await AuditLog.find()
            .sort("-created_at")
            .skip(offset)
            .limit(limit)
            .to_list()
        )
