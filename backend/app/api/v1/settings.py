"""
OpsPilot — Settings API Routes
================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.dependencies import get_db, get_current_user
from app.services.settings_service import SettingsService
from app.models.user import User

router = APIRouter()

@router.get("/audit-logs", summary="Get system audit logs (Admin only)")
async def get_audit_logs(
    page: int = 1,
    page_size: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # In a real app, enforce admin role here
    # if current_user.role != 'admin':
    #     raise HTTPException(status_code=403, detail="Not authorized")

    service = SettingsService(db)
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
                "timestamp": log.created_at.isoformat() if log.created_at else None
            } for log in logs
        ]
    }
