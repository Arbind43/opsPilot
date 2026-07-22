"""
OpsPilot — Dashboard Service
===============================
Aggregates high-level metrics and activities for the operations dashboard.
Uses Beanie ODM for MongoDB operations.
"""

from typing import Any, Dict, List

from app.models.asset import Asset
from app.models.document import Document
from app.models.incident import Incident
from app.models.maintenance import MaintenanceRecord


class DashboardService:
    """No session needed — Beanie operates directly on documents."""

    async def get_statistics(self) -> Dict[str, Any]:
        """Aggregate counts for dashboard overview."""
        total_assets = await Asset.find().count()
        total_docs = await Document.find().count()
        open_incidents = await Incident.find({"status": {"$ne": "resolved"}}).count()
        pending_maintenance = await MaintenanceRecord.find(
            {"status": "scheduled"}
        ).count()

        return {
            "total_assets": total_assets,
            "total_documents": total_docs,
            "open_incidents": open_incidents,
            "pending_maintenance": pending_maintenance,
            "system_health": 98.4,  # Placeholder — computed from active telemetry in production
        }

    async def get_recent_activity(self) -> List[Dict[str, Any]]:
        """Fetch a unified timeline of recent activities."""
        recent_incidents = (
            await Incident.find().sort("-created_at").limit(5).to_list()
        )
        activities = []
        for inc in recent_incidents:
            activities.append(
                {
                    "id": str(inc.id),
                    "type": "incident",
                    "title": inc.title,
                    "timestamp": inc.created_at.isoformat() if inc.created_at else None,
                    "severity": inc.severity,
                }
            )
        activities.sort(key=lambda x: x["timestamp"] or "", reverse=True)
        return activities

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Fetch critical alerts that require immediate attention."""
        critical_incidents = await Incident.find(
            {"severity": "critical", "status": {"$ne": "resolved"}}
        ).to_list()

        alerts = []
        for inc in critical_incidents:
            alerts.append(
                {
                    "id": str(inc.id),
                    "title": inc.title,
                    "type": "critical_incident",
                    "timestamp": (inc.occurred_at or inc.created_at).isoformat()
                    if (inc.occurred_at or inc.created_at)
                    else None,
                }
            )
        return alerts
