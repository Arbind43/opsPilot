"""
OpsPilot — Compliance Service
===============================
Runs automated compliance checks against industry standards (e.g. ISO 9001, OSHA)
using operational data and knowledge base rules.
"""

from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.incident import Incident
from app.models.maintenance import MaintenanceRecord

class ComplianceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def run_compliance_check(self) -> Dict[str, Any]:
        """
        Evaluates the current system state against compliance rules.
        In a production RAG system, this would query the vector database for 
        regulations and compare them against actual maintenance logs.
        """
        # Fetch high severity incidents
        stmt_incidents = select(Incident).where(Incident.severity == "critical", Incident.status != "closed")
        res_inc = await self.session.execute(stmt_incidents)
        critical_incidents = list(res_inc.scalars().all())

        # Fetch overdue maintenance (simplified logic for stub)
        stmt_maint = select(MaintenanceRecord).where(MaintenanceRecord.status == "scheduled")
        res_maint = await self.session.execute(stmt_maint)
        pending_maint = list(res_maint.scalars().all())

        # Run the AI Compliance Auditor
        try:
            from ai.agents.compliance_agent import ComplianceAgent
            agent = ComplianceAgent()
            report = await agent.generate_report(len(critical_incidents), len(pending_maint))
            return report
        except ImportError:
            # Fallback stub if agent is unavailable
            score = 100 - (len(critical_incidents) * 5) - (len(pending_maint) * 2)
            score = max(0, min(100, score))
            return {
                "overall_score": score,
                "status": "compliant" if score >= 90 else ("warning" if score >= 75 else "critical"),
                "evaluations": [
                    {
                        "standard": "System Stub",
                        "clause": "N/A",
                        "status": "compliant",
                        "details": "ComplianceAgent not loaded."
                    }
                ]
            }
