"""OpsPilot — Dashboard Routes"""

from fastapi import APIRouter, Depends
from app.services.dashboard_service import DashboardService
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("/stats", summary="Get dashboard statistics")
async def get_stats(
    user_id: str = Depends(get_current_user_id),
):
    service = DashboardService()
    return await service.get_statistics()


@router.get("/activity", summary="Get recent activity")
async def get_activity(
    user_id: str = Depends(get_current_user_id),
):
    service = DashboardService()
    items = await service.get_recent_activity()
    return {"items": items}


@router.get("/alerts", summary="Get active alerts")
async def get_alerts(
    user_id: str = Depends(get_current_user_id),
):
    service = DashboardService()
    items = await service.get_active_alerts()
    return {"items": items}
