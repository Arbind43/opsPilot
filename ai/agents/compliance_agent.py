"""
OpsPilot — Compliance Agent
==============================
AI Agent that evaluates procedures and questions against regulatory documents
(e.g., OSHA, ISO) using Hybrid RAG.
"""

import logging
from typing import Dict, Any, List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai.retrieval.hybrid import HybridRetriever
from ai.llm_factory import get_llm
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ComplianceEvaluation(BaseModel):
    standard: str = Field(description="The regulatory standard, e.g. ISO 9001:2015")
    clause: str = Field(description="The specific clause or requirement")
    status: str = Field(description="compliant, non-compliant, or warning")
    details: str = Field(description="Explanation of why this status was given")

class ComplianceReport(BaseModel):
    overall_score: int = Field(description="0 to 100")
    status: str = Field(description="compliant, warning, or critical")
    evaluations: List[ComplianceEvaluation]

COMPLIANCE_SYSTEM_PROMPT = """You are OpsPilot AI Compliance Agent — an expert in regulatory frameworks, quality standards, and compliance requirements across any industry.

Supported frameworks include (but are not limited to): ISO 9001, ISO 27001, HIPAA, GDPR, OSHA, EPA, SOX, PCI-DSS, FDA 21 CFR, and industry-specific regulations.

You are asked to verify compliance or answer regulatory questions based ONLY on the provided regulatory documents.

Context from Regulatory Knowledge Base:
{context}

Question/Procedure to Evaluate: {question}

Respond with:
- A clear compliance evaluation (Compliant / Non-Compliant / Needs Review)
- The specific regulatory clauses cited (adapt to whatever framework applies)
- Practical remediation steps if non-compliant
- Confidence: [High/Medium/Low]
"""

class ComplianceAgent:
    def __init__(self):
        # We use the standard hybrid retriever, but the prompt forces a compliance lens
        self.retriever = HybridRetriever()
        self._llm = None
        self._chain = None

    def _get_chain(self):
        if self._chain is None:
            llm = get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_template(COMPLIANCE_SYSTEM_PROMPT)
            self._chain = prompt | llm | StrOutputParser()
        return self._chain

    async def generate_report(self, active_incidents: int, pending_maint: int) -> dict:
        """Generates a structured compliance report using AI."""
        llm = get_llm(temperature=0.1)
        structured_llm = llm.with_structured_output(ComplianceReport)
        
        prompt = ChatPromptTemplate.from_template(
            "You are the AI Compliance Auditor for an enterprise platform. Based on the current system metrics, generate a compliance report.\n"
            "Active Critical Incidents: {incidents}\n"
            "Pending Tasks: {maint}\n\n"
            "Evaluate against relevant quality and operational standards (e.g. ISO 9001, industry-specific frameworks). "
            "If there are critical incidents, the quality standard should probably be non-compliant. "
            "If there are many pending tasks, operational safety standards might be a warning.\n"
            "Return a structured JSON report."
        )
        chain = prompt | structured_llm
        
        try:
            result = await chain.ainvoke({"incidents": active_incidents, "maint": pending_maint})
            return result.model_dump()
        except Exception as e:
            logger.error(f"Compliance report generation failed: {e}")
            return {
                "overall_score": 50,
                "status": "warning",
                "evaluations": [
                    {"standard": "System", "clause": "AI Audit", "status": "warning", "details": "AI audit failed due to API limits."}
                ]
            }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=20))
    async def _invoke_chain_with_retry(self, context_text: str, query: str) -> str:
        chain = self._get_chain()
        return await chain.ainvoke({
            "context": context_text,
            "question": query,
        })

    async def chat(self, user_id: str, query: str) -> Dict[str, Any]:
        logger.info(f"Compliance query from {user_id}: {query[:80]}")

        # 1. Retrieve context
        # We append keywords to strongly bias the vector search towards compliance documents
        search_query = query + " regulation compliance standard audit requirements policy"
        context_items: List[Dict] = await self.retriever.retrieve_context(search_query, top_k=5)

        if context_items:
            context_parts = []
            for i, item in enumerate(context_items, 1):
                source = item.get("source", item.get("type", "Knowledge Base"))
                content = item.get("content", "")
                context_parts.append(f"[{i}] ({source})\n{content}")
            context_text = "\n\n".join(context_parts)
        else:
            context_text = "No specific regulatory documents found in the knowledge base."

        # 2. Call LLM
        try:
            answer = await self._invoke_chain_with_retry(context_text, query)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            answer = f"Error during compliance check: {str(e)}"

        confidence_score = 0.9 if "High" in answer else (0.6 if "Medium" in answer else 0.4)

        return {
            "answer": answer,
            "context_used": context_items,
            "sources_count": len(context_items),
            "confidence": confidence_score,
            "agent_used": "compliance"
        }
