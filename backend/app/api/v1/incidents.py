"""
OpsPilot — Incidents API Routes
=================================
"""

from typing import List, Dict, Any
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user_id, get_db
from app.schemas.incident import IncidentResponse, IncidentCreate, IncidentUpdate
from app.services.incident_service import IncidentService
from ai.agents.rca_agent import RCAAgent

router = APIRouter()
rca_agent = RCAAgent()

@router.get("", summary="List all incidents")
async def list_incidents(
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    offset = (page - 1) * page_size
    items = await service.get_all_incidents(offset=offset, limit=page_size)
    return {
        "items": [IncidentResponse.model_validate(inc).model_dump(mode='json') for inc in items],
        "page": page,
        "page_size": page_size
    }

@router.get("/systemic-rca", summary="Generate Systemic RCA across all incidents")
async def generate_systemic_rca(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    # Fetch a large batch of recent incidents to analyze
    items = await service.get_all_incidents(offset=0, limit=50)
    
    analysis = await rca_agent.analyze_systemic_patterns(items)
    return {"analysis": analysis}

@router.post("", summary="Create new incident")
async def create_incident(
    data: IncidentCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    incident = await service.create_incident(data.dict(), user_id)
    return {"id": str(incident.id), "status": "created"}

@router.post("/{incident_id}/rca", summary="Generate RCA for incident")
async def generate_rca(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    incident = await service.get_incident(incident_id)
    
    asset_name = incident.asset.name if incident.asset else "Unknown Equipment"
    
    # Generate RCA using agent
    rca_result = await rca_agent.generate_rca(
        incident_title=incident.title,
        incident_desc=incident.description or "",
        asset_name=asset_name
    )
    
    # Update incident with root cause
    await service.update_incident(incident_id, {"root_cause": rca_result})
    
    return rca_result
