"""
OpsPilot — Compliance Service
===============================
Runs automated compliance checks against industry standards (e.g. ISO 9001, OSHA)
using operational data and knowledge base rules.
Uses Beanie ODM for MongoDB operations.
"""

from typing import Dict, Any

from app.models.incident import Incident
from app.models.maintenance import MaintenanceRecord


class ComplianceService:
    """No session needed — Beanie operates directly on documents."""

    async def run_compliance_check(self) -> Dict[str, Any]:
        """
        Evaluates the current system state against compliance rules.
        In a production RAG system, this would query the vector database for
        regulations and compare them against actual maintenance logs.
        """
        # Fetch high severity incidents
        critical_incidents = await Incident.find(
            {"severity": "critical", "status": {"$ne": "closed"}}
        ).to_list()

        # Fetch pending maintenance
        pending_maint = await MaintenanceRecord.find(
            {"status": "scheduled"}
        ).to_list()

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
                        "details": "ComplianceAgent not loaded.",
                    }
                ],
            }
