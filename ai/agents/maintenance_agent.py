"""
OpsPilot — Predictive Maintenance Agent
======================================
Analyzes an asset's timeline (incidents, maintenance) and generates 
a predictive failure risk score using structured LLM output.
"""

import logging
from typing import List, Dict, Any

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from ai.llm_factory import get_llm
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class PredictiveAnalysisResponse(BaseModel):
    failure_risk_score: int = Field(description="A score from 0 to 100 representing the likelihood of asset failure in the near future. 0 = perfect condition, 100 = imminent failure.")
    trend: str = Field(description="The trend of the asset condition. Must be exactly one of: 'improving', 'stable', 'degrading'.")
    recommendations: List[str] = Field(description="A list of 2-3 short, actionable maintenance recommendations based on the history.")

PREDICTIVE_SYSTEM_PROMPT = """You are OpsPilot AI Predictive Intelligence Agent — an expert in operational risk analysis for any industry domain.

You will be given the operational history (incidents, tasks, inspections, events) of an enterprise resource.
Your job is to analyze this history and predict the resource's risk of failure or degradation.

Consider the following factors:
- Frequency of recent incidents or issues.
- Types of tasks performed (corrective vs preventive).
- Any noted degradation in inspections or reviews.
- Time since last maintenance or review event.

Resource Name: {asset_name}
Resource Type: {asset_type}
Status: {status}

Timeline History (Most recent first):
{timeline_text}

Output your analysis following the requested schema. Ensure the recommendations are actionable for the given resource type.
"""

class MaintenanceAgent:
    def __init__(self):
        self._llm = None
        self._chain = None

    def _get_chain(self):
        if self._chain is None:
            # Use model from settings (GEMINI_MODEL in .env)
            llm = get_llm(temperature=0.2)
            structured_llm = llm.with_structured_output(PredictiveAnalysisResponse)
            prompt = ChatPromptTemplate.from_template(PREDICTIVE_SYSTEM_PROMPT)
            self._chain = prompt | structured_llm
        return self._chain

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=20))
    async def _invoke_chain_with_retry(self, inputs: dict):
        chain = self._get_chain()
        return await chain.ainvoke(inputs)

    async def analyze_asset_risk(self, asset: Any, timeline_events: List[Any]) -> PredictiveAnalysisResponse:
        """
        Takes an asset dict/object and its timeline events, 
        returns a structured PredictiveAnalysisResponse.
        """
        # Format timeline for the LLM
        if not timeline_events:
            timeline_text = "No operational history recorded. Asset is either new or tracking has not started."
        else:
            parts = []
            for ev in timeline_events:
                # Handle both dict and pydantic models
                ev_type = ev.get('event_type') if isinstance(ev, dict) else getattr(ev, 'event_type', 'event')
                title = ev.get('title') if isinstance(ev, dict) else getattr(ev, 'title', '')
                timestamp = ev.get('timestamp') if isinstance(ev, dict) else getattr(ev, 'timestamp', '')
                desc = ev.get('description') if isinstance(ev, dict) else getattr(ev, 'description', '')
                
                parts.append(f"[{timestamp}] {str(ev_type).upper()}: {title}")
                if desc:
                    parts.append(f"  Details: {desc}")
            timeline_text = "\n".join(parts)

        # Handle asset dict vs object
        asset_name = asset.get('name') if isinstance(asset, dict) else getattr(asset, 'name', 'Unknown')
        asset_type = asset.get('asset_type') if isinstance(asset, dict) else getattr(asset, 'asset_type', 'Unknown')
        status = asset.get('status') if isinstance(asset, dict) else getattr(asset, 'status', 'Unknown')

        try:
            response = await self._invoke_chain_with_retry({
                "asset_name": asset_name,
                "asset_type": asset_type,
                "status": status,
                "timeline_text": timeline_text
            })
            return response
        except Exception as e:
            logger.error(f"MaintenanceAgent failed: {e}")
            # Fallback safe response if rate limit fails
            return PredictiveAnalysisResponse(
                failure_risk_score=50,
                trend="stable",
                recommendations=["Schedule baseline inspection (AI analysis currently unavailable due to system limits)"]
            )
