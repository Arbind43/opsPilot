"""
OpsPilot — Settings and Audit Log Service
===========================================
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class SettingsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_audit_logs(self, offset: int = 0, limit: int = 100) -> List[AuditLog]:
        stmt = (
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # We could add methods here to handle application settings in the DB if needed.
    # For now, we mainly expose Audit Logs as requested.
