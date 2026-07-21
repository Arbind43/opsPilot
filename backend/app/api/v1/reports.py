"""
OpsPilot — Reports API Routes
===============================
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user_id, get_db
from app.services.report_service import ReportService

router = APIRouter()

class ReportCreate(BaseModel):
    title: str
    report_type: str = "summary"
    asset_id: Optional[UUID] = None

@router.get("", summary="List all generated reports")
async def list_reports(
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    offset = (page - 1) * page_size
    reports = await service.get_all_reports(offset=offset, limit=page_size)
    
    return {
        "items": [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.report_type,
                "status": r.status,
                "asset_name": r.asset.name if r.asset else "All Assets",
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "content": r.content
            } for r in reports
        ]
    }

@router.post("/generate", summary="Generate a new AI report")
async def generate_report(
    data: ReportCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    report = await service.generate_report(data.dict(), user_id)
    return {"id": str(report.id), "status": report.status, "content": report.content}

@router.delete("/{report_id}", summary="Delete a report")
async def delete_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    await service.delete_report(report_id)
    return {"status": "deleted"}
