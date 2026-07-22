"""
OpsPilot — Compliance API Routes
==================================
"""

from fastapi import APIRouter, Depends

from app.services.compliance_service import ComplianceService
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("/report", summary="Generate automated compliance report")
async def get_compliance_report(
    user_id: str = Depends(get_current_user_id),
):
    service = ComplianceService()
    report = await service.run_compliance_check()
    return report
