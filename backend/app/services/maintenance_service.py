"""
OpsPilot — Maintenance Service
================================
Business logic for managing maintenance records and predictive schedules.
"""

from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.maintenance import MaintenanceRecord
from app.models.asset import Asset
from app.core.exceptions import NotFoundError

class MaintenanceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_records(self, offset: int = 0, limit: int = 50) -> List[MaintenanceRecord]:
        stmt = (
            select(MaintenanceRecord)
            .options(selectinload(MaintenanceRecord.asset))
            .order_by(MaintenanceRecord.scheduled_at.desc().nullslast())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_record(self, record_id: UUID) -> MaintenanceRecord:
        stmt = (
            select(MaintenanceRecord)
            .options(selectinload(MaintenanceRecord.asset))
            .where(MaintenanceRecord.id == record_id)
        )
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            raise NotFoundError("Maintenance record not found")
        return record

    async def create_record(self, data: Dict[str, Any], user_id: UUID) -> MaintenanceRecord:
        record = MaintenanceRecord(
            title=data["title"],
            description=data.get("description"),
            maintenance_type=data.get("maintenance_type", "preventive"),
            status=data.get("status", "scheduled"),
            asset_id=data["asset_id"],
            performed_by=user_id if data.get("status") in ["in_progress", "completed"] else None,
            scheduled_at=data.get("scheduled_at"),
            cost=data.get("cost")
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def update_record(self, record_id: UUID, data: Dict[str, Any]) -> MaintenanceRecord:
        record = await self.get_record(record_id)
        
        for key, value in data.items():
            if hasattr(record, key) and key != "id":
                setattr(record, key, value)
                
        await self.session.commit()
        await self.session.refresh(record)
        return record
