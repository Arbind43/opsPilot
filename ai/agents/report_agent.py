"""
OpsPilot — AI Report Agent
=============================
Generates comprehensive narrative reports by synthesizing data from across the platform.
"""

import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai.llm_factory import get_llm

logger = logging.getLogger(__name__)

REPORT_PROMPT = """You are OpsPilot's Chief Reporting AI. 

Write an "Executive Summary" for an operational performance report.

Data Context:
- Active Incidents: {incidents_count}
- Assets Tracked: {assets_count}
- Completed Maintenance: {maint_count}
- Overall System Status: {system_status}

Write a professional, 2-3 paragraph summary highlighting what these numbers mean for plant reliability and safety. If there are active incidents, mention the need for attention.
"""

class ReportAgent:
    def __init__(self):
        pass

    async def generate_executive_summary(self, data: dict) -> str:
        """Generates a natural language summary for the report."""
        llm = get_llm(temperature=0.3)
        prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)
        chain = prompt | llm | StrOutputParser()
        
        try:
            return await chain.ainvoke(data)
        except Exception as e:
            logger.error(f"Failed to generate report summary: {e}")
            return "Executive summary generation failed due to an AI system error."
