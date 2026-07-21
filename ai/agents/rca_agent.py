"""
OpsPilot — Root Cause Analysis Agent
=======================================
LangChain-powered RCA agent that analyses incidents using the knowledge base.
Produces structured RCA reports with probable causes, evidence, and recommendations.
"""

import logging
from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai.retrieval.hybrid import HybridRetriever
from ai.llm_factory import get_llm

logger = logging.getLogger(__name__)

RCA_PROMPT = """You are an expert Root Cause Analysis (RCA) specialist for enterprise operations — adaptable to any industry domain.

You are investigating the following incident/event:

INCIDENT TITLE: {incident_title}
RESOURCE AFFECTED: {asset_name}
INCIDENT DESCRIPTION: {incident_desc}

RELEVANT KNOWLEDGE BASE CONTEXT:
{context}

Based on the above, produce a structured RCA report with these sections:

## 1. Incident Summary
Brief summary of what happened.

## 2. Probable Root Causes
List 2-4 probable root causes ranked by likelihood. For each cause:
- **Cause**: [description]
- **Evidence**: [what in the context or incident supports this]
- **Likelihood**: [High/Medium/Low]

## 3. Contributing Factors
Secondary factors that may have contributed.

## 4. Recommended Corrective Actions
Numbered list of specific, actionable steps to fix the root cause and prevent recurrence.

## 5. Preventive Measures
Long-term recommendations to prevent similar incidents.

## 6. Sources Consulted
List the knowledge base sources used.

## 7. Confidence Assessment
Overall confidence in this RCA: [High/Medium/Low] — [reason]
"""

SYSTEMIC_PATTERN_PROMPT = """You are OpsPilot's Chief Reliability AI — an enterprise-wide intelligence engine for any industry. 

You are analyzing the entire incident and event history for the organization to identify systemic failure patterns.
Here is a list of historical incidents:

{incidents_text}

Analyze the above data and provide a "Systemic Pattern Analysis Report". Include:
1. **Recurring Root Causes**: What underlying issues are driving multiple incidents?
2. **High-Risk Resources/Areas**: Are specific resources, departments, or processes over-represented?
3. **Temporal/Process Trends**: Are failures happening at specific times, or during specific processes?
4. **Strategic Recommendations**: What organization-wide changes are needed to reduce these patterns?

Format your response as a professional executive summary using Markdown.
"""

class RCAAgent:
    def __init__(self):
        self.retriever = HybridRetriever()
        self._chain = None

    def _get_chain(self):
        if self._chain is None:
            llm = get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_template(RCA_PROMPT)
            self._chain = prompt | llm | StrOutputParser()
        return self._chain

    async def generate_rca(
        self,
        incident_title: str,
        incident_desc: str,
        asset_name: str,
    ) -> Dict[str, Any]:
        """
        Retrieves context about the asset and incident, then formulates an RCA report.
        """
        logger.info(f"Generating RCA for: {incident_title}")

        # Build a rich query combining asset + incident details
        query = (
            f"Root cause analysis for: {incident_title}. "
            f"Resource: {asset_name}. "
            f"Description: {incident_desc}. "
            f"operational history, failure modes, inspection findings, documentation"
        )

        context_items = await self.retriever.retrieve_context(query, top_k=7)

        # Format context
        if context_items:
            context_parts = []
            for i, item in enumerate(context_items, 1):
                source = item.get("source", item.get("type", "Knowledge Base"))
                content = item.get("content", "")
                context_parts.append(f"[{i}] Source: {source}\n{content}")
            context_text = "\n\n".join(context_parts)
        else:
            context_text = (
                "No specific historical records found in the knowledge base. "
                "RCA will be based on general engineering principles."
            )

        try:
            chain = self._get_chain()
            rca_text = await chain.ainvoke({
                "incident_title": incident_title,
                "asset_name": asset_name,
                "incident_desc": incident_desc,
                "context": context_text,
            })
        except Exception as e:
            logger.error(f"RCA LLM call failed: {e}")
            rca_text = (
                f"## RCA Generation Error\n\n"
                f"Retrieved {len(context_items)} relevant documents but encountered an LLM error.\n"
                f"Error: {str(e)}\n\n"
                f"Please check the API key configuration."
            )

        confidence = 0.85 if context_items else 0.45

        return {
            "root_cause_analysis": rca_text,
            "confidence": confidence,
            "sources_consulted": len(context_items),
            "context_used": context_items,
        }
        
    async def analyze_systemic_patterns(self, incidents: list) -> str:
        """
        Analyzes a list of historical incidents to identify systemic patterns.
        """
        logger.info(f"Analyzing {len(incidents)} incidents for systemic patterns.")
        
        if not incidents:
            return "No historical incidents found to analyze."
            
        # Format incidents
        parts = []
        for inc in incidents:
            title = inc.get("title") if isinstance(inc, dict) else inc.title
            desc = inc.get("description") if isinstance(inc, dict) else inc.description
            severity = inc.get("severity") if isinstance(inc, dict) else inc.severity
            status = inc.get("status") if isinstance(inc, dict) else inc.status
            date = inc.get("created_at") if isinstance(inc, dict) else getattr(inc, "created_at", "Unknown Date")
            
            parts.append(f"- [{date}] [{severity.upper()}] {title}: {desc} (Status: {status})")
            
        incidents_text = "\n".join(parts)
        
        llm = get_llm(temperature=0.2)
        prompt = ChatPromptTemplate.from_template(SYSTEMIC_PATTERN_PROMPT)
        chain = prompt | llm | StrOutputParser()
        
        try:
            result = await chain.ainvoke({"incidents_text": incidents_text})
            return result
        except Exception as e:
            logger.error(f"Systemic pattern analysis failed: {e}")
            return f"Failed to generate systemic pattern analysis due to AI system error: {str(e)}"
