"""
OpsPilot — Maintenance Service
================================
Business logic for managing maintenance records and predictive schedules.
Uses Beanie ODM for MongoDB operations.
"""

from typing import List, Dict, Any
from uuid import UUID

from app.models.maintenance import MaintenanceRecord
from app.core.exceptions import NotFoundError


class MaintenanceService:
    """No session needed — Beanie operates directly on documents."""

    async def get_all_records(self, offset: int = 0, limit: int = 50) -> List[MaintenanceRecord]:
        return (
            await MaintenanceRecord.find()
            .sort("-created_at")
            .skip(offset)
            .limit(limit)
            .to_list()
        )

    async def get_record(self, record_id: UUID) -> MaintenanceRecord:
        record = await MaintenanceRecord.get(record_id)
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
            cost=data.get("cost"),
        )
        await record.insert()
        return record

    async def update_record(self, record_id: UUID, data: Dict[str, Any]) -> MaintenanceRecord:
        record = await self.get_record(record_id)
        for key, value in data.items():
            if hasattr(record, key) and key != "id":
                setattr(record, key, value)
        await record.save()
        return record
