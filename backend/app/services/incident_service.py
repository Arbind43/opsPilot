"""
OpsPilot — Incident Service
=============================
Handles business logic for incidents and anomaly reports.
Uses Beanie 2.x ODM for MongoDB operations.
"""

from typing import List, Dict, Any
from uuid import UUID

from app.models.incident import Incident
from app.core.exceptions import NotFoundError


class IncidentService:

    async def get_all_incidents(self, offset: int = 0, limit: int = 50) -> List[Incident]:
        return await Incident.find().sort("-created_at").skip(offset).limit(limit).to_list()

    async def get_incident(self, incident_id: UUID) -> Incident:
        incident = await Incident.get(incident_id)
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
            reported_by=user_id,
        )
        await incident.insert()
        return incident

    async def update_incident(self, incident_id: UUID, data: Dict[str, Any]) -> Incident:
        incident = await self.get_incident(incident_id)
        for key, value in data.items():
            if hasattr(incident, key) and key != "id":
                setattr(incident, key, value)
        await incident.save()
        return incident
