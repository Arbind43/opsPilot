"""
OpsPilot — Maintenance API Routes
===================================
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

from app.services.maintenance_service import MaintenanceService
from app.dependencies import get_current_user_id

router = APIRouter()


class MaintenanceCreate(BaseModel):
    title: str
    description: str = ""
    maintenance_type: str = "preventive"
    status: str = "scheduled"
    asset_id: UUID
    scheduled_at: Optional[datetime] = None
    cost: Optional[float] = None


@router.get("", summary="List all maintenance records")
async def list_records(
    page: int = 1,
    page_size: int = 50,
    user_id: str = Depends(get_current_user_id),
):
    service = MaintenanceService()
    offset = (page - 1) * page_size
    records = await service.get_all_records(offset=offset, limit=page_size)

    return {
        "items": [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.maintenance_type,
                "status": r.status,
                "asset_id": str(r.asset_id),
                "scheduled_at": r.scheduled_at.isoformat() if r.scheduled_at else None,
            }
            for r in records
        ]
    }


@router.post("", summary="Create a new maintenance record")
async def create_record(
    data: MaintenanceCreate,
    user_id: UUID = Depends(get_current_user_id),
):
    service = MaintenanceService()
    record = await service.create_record(data.dict(), user_id)
    return {"id": str(record.id), "status": record.status}
