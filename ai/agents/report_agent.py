"""
OpsPilot — AI Report Agent
=============================
Generates comprehensive narrative reports by synthesizing data from across the platform.
"""

import logging
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from ai.llm_factory import get_llm

logger = logging.getLogger(__name__)

class ReportOutput(BaseModel):
    executive_summary: str = Field(description="A professional, 2-3 paragraph summary highlighting what the metrics and context mean for reliability and safety.")
    recommendations: List[str] = Field(description="2-4 actionable recommendations based on the findings.")

class ReportAgent:
    def __init__(self):
        from ai.retrieval.hybrid import HybridRetriever
        self.retriever = HybridRetriever()

    async def generate_executive_summary(self, data: dict) -> dict:
        """Generates a natural language summary and recommendations for the report."""
        
        # 1. Retrieve relevant context for the executive summary
        search_query = "overall operational performance, safety procedures, critical incidents, maintenance logs"
        context_items = await self.retriever.retrieve_context(search_query, top_k=5)
        
        context_text = "No operational documents found."
        if context_items:
            context_parts = []
            for i, item in enumerate(context_items, 1):
                source = item.get("source", item.get("type", "Knowledge Base"))
                content = item.get("content", "")
                context_parts.append(f"[{i}] ({source})\n{content}")
            context_text = "\n\n".join(context_parts)

        llm = get_llm(temperature=0.3)
        structured_llm = llm.with_structured_output(ReportOutput)
        
        prompt = ChatPromptTemplate.from_template(
            "You are OpsPilot's Chief Reporting AI.\n\n"
            "Write an 'Executive Summary' and provide 'Recommendations' for an operational performance report based on the uploaded data.\n\n"
            "Current Data Metrics:\n"
            "- Active Incidents: {incidents_count}\n"
            "- Assets Tracked: {assets_count}\n"
            "- Completed Maintenance: {maint_count}\n"
            "- Overall System Status: {system_status}\n\n"
            "Retrieved Operational Context (Actual Uploaded Data):\n{context}\n\n"
            "Write a professional summary and specific recommendations."
        )
        chain = prompt | structured_llm
        
        try:
            data["context"] = context_text
            result = await chain.ainvoke(data)
            return result.model_dump()
        except Exception as e:
            logger.error(f"Failed to generate report summary: {e}")
            return {
                "executive_summary": "Executive summary generation failed due to an AI system error.",
                "recommendations": ["Review system logs for errors."]
            }
