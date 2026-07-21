"""
OpsPilot — Maintenance API Routes
===================================
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user_id, get_db
from app.services.maintenance_service import MaintenanceService

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
    db: AsyncSession = Depends(get_db)
):
    service = MaintenanceService(db)
    offset = (page - 1) * page_size
    records = await service.get_all_records(offset=offset, limit=page_size)
    
    return {
        "items": [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.maintenance_type,
                "status": r.status,
                "asset_name": r.asset.name if r.asset else "Unknown Asset",
                "scheduled_at": r.scheduled_at.isoformat() if r.scheduled_at else None
            } for r in records
        ]
    }

@router.post("", summary="Create a new maintenance record")
async def create_record(
    data: MaintenanceCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = MaintenanceService(db)
    record = await service.create_record(data.dict(), user_id)
    return {"id": str(record.id), "status": record.status}
