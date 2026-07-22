"""
OpsPilot — Asset Routes
=========================
CRUD operations for industrial assets and asset hierarchy.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.asset import AssetResponse, AssetCreate, AssetUpdate
from app.services.asset_service import AssetService
from app.dependencies import get_current_user_id
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=dict, summary="List assets")
async def list_assets(
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    offset = (page - 1) * page_size
    items = await service.get_all_assets(offset=offset, limit=page_size)
    return {
        "items": [AssetResponse.model_validate(asset).model_dump(mode="json") for asset in items],
        "page": page,
        "page_size": page_size,
    }


@router.post("", response_model=AssetResponse, status_code=201, summary="Create asset")
async def create_asset(
    data: AssetCreate,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    return await service.create_asset(data)


@router.get("/tree", summary="Get asset hierarchy tree")
async def get_asset_tree(
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    tree = await service.get_asset_tree()
    return {"children": tree}


@router.get("/{asset_id}", response_model=AssetResponse, summary="Get asset detail")
async def get_asset(
    asset_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    asset = await service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetResponse, summary="Update asset")
async def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    asset = await service.update_asset(asset_id, data)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}", status_code=204, summary="Delete asset")
async def delete_asset(
    asset_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    success = await service.delete_asset(asset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return None


@router.get("/{asset_id}/timeline", summary="Get asset timeline")
async def get_asset_timeline(
    asset_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()
    events = await service.get_timeline(asset_id)
    return {"events": events}


@router.get("/{asset_id}/predictive-analysis", summary="Get predictive maintenance analysis")
async def get_predictive_analysis(
    asset_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = AssetService()

    # 1. Get Asset
    asset = await service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # 2. Get Timeline
    events = await service.get_timeline(asset_id)

    # 3. Call AI Agent
    try:
        from ai.agents.maintenance_agent import MaintenanceAgent
        agent = MaintenanceAgent()
        analysis = await agent.analyze_asset_risk(asset, events)
        return analysis.model_dump()
    except ImportError:
        logger.warning("MaintenanceAgent not available. Returning stub.")
        return {
            "failure_risk_score": 50,
            "trend": "stable",
            "recommendations": ["Agent unavailable - check module imports"],
        }
    except Exception as e:
        logger.error(f"Predictive analysis failed: {e}")
        return {
            "failure_risk_score": 50,
            "trend": "stable",
            "recommendations": ["Analysis failed due to a system error. Please try again."],
        }
