"""
OpsPilot — Settings API Routes
================================
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from app.services.settings_service import SettingsService
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("/audit-logs", summary="Get system audit logs")
async def get_audit_logs(
    page: int = 1,
    page_size: int = 100,
    user_id: str = Depends(get_current_user_id),
):
    service = SettingsService()
    offset = (page - 1) * page_size
    logs = await service.get_audit_logs(offset=offset, limit=page_size)

    return {
        "items": [
            {
                "id": str(log.id),
                "user_id": str(log.user_id),
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": str(log.resource_id) if log.resource_id else None,
                "details": log.details,
                "ip_address": log.ip_address,
                "timestamp": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ]
    }
