"""
OpsPilot — Dashboard Service
===============================
Aggregates high-level metrics and activities for the operations dashboard.
"""

from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.asset import Asset
from app.models.document import Document
from app.models.incident import Incident
from app.models.maintenance import MaintenanceRecord
from app.models.inspection import Inspection

class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_statistics(self) -> Dict[str, Any]:
        """Aggregate counts for dashboard overview."""
        # Execute queries concurrently if possible, but for simplicity we'll do sequentially
        total_assets = await self.session.execute(select(func.count(Asset.id)))
        total_docs = await self.session.execute(select(func.count(Document.id)))
        open_incidents = await self.session.execute(
            select(func.count(Incident.id)).where(Incident.status != "resolved")
        )
        pending_maintenance = await self.session.execute(
            select(func.count(MaintenanceRecord.id)).where(MaintenanceRecord.status == "scheduled")
        )

        return {
            "total_assets": total_assets.scalar() or 0,
            "total_documents": total_docs.scalar() or 0,
            "open_incidents": open_incidents.scalar() or 0,
            "pending_maintenance": pending_maintenance.scalar() or 0,
            "system_health": 98.4  # Mocked placeholder, normally computed from active telemetry
        }

    async def get_recent_activity(self) -> List[Dict[str, Any]]:
        """Fetch a unified timeline of recent activities."""
        # For a true unified feed, you'd typically union tables or use a dedicated AuditLog table.
        # We will mock a feed by pulling recent incidents and maintenance.
        recent_incidents = await self.session.execute(
            select(Incident).order_by(Incident.created_at.desc()).limit(3)
        )
        activities = []
        for inc in recent_incidents.scalars():
            activities.append({
                "id": str(inc.id),
                "type": "incident",
                "title": inc.title,
                "timestamp": inc.created_at,
                "severity": inc.severity
            })
            
        # Sort combined list by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Fetch critical alerts that require immediate attention."""
        critical_incidents = await self.session.execute(
            select(Incident).where(Incident.severity == "critical", Incident.status != "resolved")
        )
        alerts = []
        for inc in critical_incidents.scalars():
            alerts.append({
                "id": str(inc.id),
                "title": inc.title,
                "type": "critical_incident",
                "timestamp": inc.occurred_at or inc.created_at
            })
        return alerts
