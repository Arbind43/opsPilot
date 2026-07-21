"""
OpsPilot — Incident Service
=============================
Handles business logic for incidents and anomaly reports.
"""

from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.incident import Incident
from app.models.asset import Asset
from app.core.exceptions import NotFoundError

class IncidentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_incidents(self, offset: int = 0, limit: int = 50) -> List[Incident]:
        stmt = (
            select(Incident)
            .options(selectinload(Incident.asset))
            .order_by(Incident.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_incident(self, incident_id: UUID) -> Incident:
        stmt = (
            select(Incident)
            .options(selectinload(Incident.asset))
            .where(Incident.id == incident_id)
        )
        result = await self.session.execute(stmt)
        incident = result.scalar_one_or_none()
        if not incident:
            raise NotFoundError("Incident not found")
        return incident

    async def create_incident(self, data: Dict[str, Any], user_id: UUID) -> Incident:
        incident = Incident(
            title=data["title"],
            description=data.get("description"),
            severity=data.get("severity", "medium"),
            status="open",
            asset_id=data["asset_id"],
            reported_by=user_id
        )
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def update_incident(self, incident_id: UUID, data: Dict[str, Any]) -> Incident:
        incident = await self.get_incident(incident_id)
        
        for key, value in data.items():
            if hasattr(incident, key) and key != "id":
                setattr(incident, key, value)
                
        await self.session.commit()
        await self.session.refresh(incident)
        return incident
