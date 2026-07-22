"""
OpsPilot — Report Service
===========================
Service for managing reporting engine operations.
Uses Beanie ODM for MongoDB operations.
"""

from typing import List, Dict, Any
from uuid import UUID

from app.models.report import Report
from app.core.exceptions import NotFoundError


class ReportService:
    """No session needed — Beanie operates directly on documents."""

    async def get_all_reports(self, offset: int = 0, limit: int = 50) -> List[Report]:
        return (
            await Report.find()
            .sort("-created_at")
            .skip(offset)
            .limit(limit)
            .to_list()
        )

    async def get_report(self, report_id: UUID) -> Report:
        report = await Report.get(report_id)
        if not report:
            raise NotFoundError("Report not found")
        return report

    async def generate_report(self, data: Dict[str, Any], user_id: UUID) -> Report:
        from app.models.incident import Incident
        from app.models.maintenance import MaintenanceRecord
        from app.models.asset import Asset

        # 1. Gather stats using Beanie
        incidents_count = await Incident.find({"status": {"$ne": "closed"}}).count()
        maint_count = await MaintenanceRecord.find({"status": "completed"}).count()
        assets_count = await Asset.find().count()

        # 2. Call AI Report Agent
        data_payload = {
            "incidents_count": incidents_count,
            "assets_count": assets_count,
            "maint_count": maint_count,
            "system_status": "Warning" if incidents_count > 0 else "Optimal",
        }

        try:
            from ai.agents.report_agent import ReportAgent
            agent = ReportAgent()
            executive_summary = await agent.generate_executive_summary(data_payload)
        except Exception as e:
            executive_summary = f"Summary generation failed: {str(e)}"

        # 3. Construct report data
        report_data = {
            "title": data.get("title", "OpsPilot Operational Report"),
            "type": data.get("report_type", "summary"),
            "executive_summary": executive_summary,
            "metrics": {"uptime": "99.8%", "incidents": incidents_count},
            "recommendations": [
                "Conduct routine visual inspection.",
                "Check log anomalies.",
            ],
        }

        report = Report(
            title=data.get("title", "OpsPilot Operational Report"),
            report_type=data.get("report_type", "summary"),
            status="generated",
            content=report_data,
            asset_id=data.get("asset_id"),
            generated_by=user_id,
        )
        await report.insert()
        return report

    async def delete_report(self, report_id: UUID) -> bool:
        report = await self.get_report(report_id)
        await report.delete()
        return True
