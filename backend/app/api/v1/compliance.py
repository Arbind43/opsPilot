"""
OpsPilot — Compliance API Routes
==================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.services.compliance_service import ComplianceService

router = APIRouter()

@router.get("/report", summary="Generate automated compliance report")
async def get_compliance_report(
    db: AsyncSession = Depends(get_db)
):
    service = ComplianceService(db)
    report = await service.run_compliance_check()
    return report
