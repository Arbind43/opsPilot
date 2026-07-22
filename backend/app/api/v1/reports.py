"""
OpsPilot — Reports API Routes
===============================
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

from app.services.report_service import ReportService
from app.dependencies import get_current_user_id

router = APIRouter()


class ReportCreate(BaseModel):
    title: str
    report_type: str = "summary"
    asset_id: Optional[UUID] = None


@router.get("", summary="List all generated reports")
async def list_reports(
    page: int = 1,
    page_size: int = 50,
    user_id: str = Depends(get_current_user_id),
):
    service = ReportService()
    offset = (page - 1) * page_size
    reports = await service.get_all_reports(offset=offset, limit=page_size)

    return {
        "items": [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.report_type,
                "status": r.status,
                "asset_id": str(r.asset_id) if r.asset_id else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "content": r.content,
            }
            for r in reports
        ]
    }


@router.post("/generate", summary="Generate a new AI report")
async def generate_report(
    data: ReportCreate,
    user_id: UUID = Depends(get_current_user_id),
):
    service = ReportService()
    report = await service.generate_report(data.dict(), user_id)
    return {"id": str(report.id), "status": report.status, "content": report.content}


@router.delete("/{report_id}", summary="Delete a report")
async def delete_report(
    report_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = ReportService()
    await service.delete_report(report_id)
    return {"status": "deleted"}
