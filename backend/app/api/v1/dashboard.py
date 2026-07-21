"""OpsPilot — Dashboard Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user_id, get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/stats", summary="Get dashboard statistics")
async def get_stats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = DashboardService(db)
    return await service.get_statistics()


@router.get("/activity", summary="Get recent activity")
async def get_activity(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = DashboardService(db)
    items = await service.get_recent_activity()
    return {"items": items}


@router.get("/alerts", summary="Get active alerts")
async def get_alerts(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = DashboardService(db)
    items = await service.get_active_alerts()
    return {"items": items}
