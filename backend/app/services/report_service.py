"""
OpsPilot — Report Service
===========================
Service for managing reporting engine operations.
"""

from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.report import Report
from app.models.asset import Asset
from app.core.exceptions import NotFoundError

class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_reports(self, offset: int = 0, limit: int = 50) -> List[Report]:
        stmt = (
            select(Report)
            .options(selectinload(Report.asset))
            .order_by(Report.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_report(self, report_id: UUID) -> Report:
        stmt = (
            select(Report)
            .options(selectinload(Report.asset))
            .where(Report.id == report_id)
        )
        result = await self.session.execute(stmt)
        report = result.scalar_one_or_none()
        if not report:
            raise NotFoundError("Report not found")
        return report

    async def generate_report(self, data: Dict[str, Any], user_id: UUID) -> Report:
        from app.models.incident import Incident
        from app.models.maintenance import MaintenanceRecord
        from sqlalchemy import func

        # 1. Gather stats
        incidents_res = await self.session.execute(select(func.count()).select_from(Incident).where(Incident.status != 'closed'))
        incidents_count = incidents_res.scalar() or 0

        maint_res = await self.session.execute(select(func.count()).select_from(MaintenanceRecord).where(MaintenanceRecord.status == 'completed'))
        maint_count = maint_res.scalar() or 0
        
        assets_res = await self.session.execute(select(func.count()).select_from(Asset))
        assets_count = assets_res.scalar() or 0

        # 2. Call AI Report Agent
        data_payload = {
            "incidents_count": incidents_count,
            "assets_count": assets_count,
            "maint_count": maint_count,
            "system_status": "Warning" if incidents_count > 0 else "Optimal"
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
            "recommendations": ["Conduct routine visual inspection.", "Check log anomalies."]
        }

        report = Report(
            title=data.get("title", "OpsPilot Operational Report"),
            report_type=data.get("report_type", "summary"),
            status="generated",
            content=report_data,
            asset_id=data.get("asset_id"),
            generated_by=user_id
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def delete_report(self, report_id: UUID) -> bool:
        report = await self.get_report(report_id)
        await self.session.delete(report)
        await self.session.commit()
        return True
