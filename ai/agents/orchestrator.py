"""
OpsPilot — Agent Orchestrator
================================
LangGraph-based multi-agent workflow supervisor.
Routes queries to the appropriate specialized agent.
"""

import logging
from typing import Any, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from ai.llm_factory import get_llm
from ai.agents.copilot_agent import CopilotAgent
from ai.agents.compliance_agent import ComplianceAgent

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    query: str
    user_id: str
    agent_used: str
    response: dict[str, Any]

class AgentOrchestrator:
    """
    LangGraph supervisor that routes user queries to specialized agents.
    """
    def __init__(self):
        self.copilot = CopilotAgent()
        self.compliance = ComplianceAgent()
        
        # Build LangGraph workflow
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("route", self.route_query)
        workflow.add_node("copilot", self.call_copilot)
        workflow.add_node("compliance", self.call_compliance)
        
        # Add edges
        workflow.add_edge(START, "route")
        
        # Conditional edge based on the 'agent_used' state key
        workflow.add_conditional_edges(
            "route",
            lambda state: state["agent_used"],
            {
                "copilot": "copilot",
                "compliance": "compliance"
            }
        )
        
        workflow.add_edge("copilot", END)
        workflow.add_edge("compliance", END)
        
        self.graph = workflow.compile()

    async def route_query(self, state: AgentState):
        """Uses LLM to determine the intent and route to the correct agent."""
        try:
            llm = get_llm(temperature=0.0)
            prompt = ChatPromptTemplate.from_template(
                "You are an intelligent routing agent for an enterprise knowledge platform. "
                "Given the user query, return exactly ONE word representing the best agent to handle it:\n"
                "- 'compliance' (for questions about regulations, standards, audits, compliance requirements, legal, quality standards, safety rules)\n"
                "- 'copilot' (for ALL other questions, including operations, general knowledge, procedures, history, analysis)\n\n"
                "Query: {query}\n\nAgent:"
            )
            chain = prompt | llm
            result = await chain.ainvoke({"query": state["query"]})
            agent_str = result.content.strip().lower()
            
            if "compliance" in agent_str:
                return {"agent_used": "compliance"}
        except Exception as e:
            logger.error(f"Routing failed: {e}")
            
        return {"agent_used": "copilot"}

    async def call_copilot(self, state: AgentState):
        res = await self.copilot.chat(state["user_id"], state["query"])
        return {"response": res}

    async def call_compliance(self, state: AgentState):
        res = await self.compliance.chat(state["user_id"], state["query"])
        return {"response": res}

    async def process_query(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Process a user query through the LangGraph orchestration pipeline.
        """
        logger.info(f"Orchestrator received query: {query[:100]}")
        
        initial_state = {
            "query": query,
            "user_id": context.get("user_id", "anonymous") if context else "anonymous",
            "agent_used": "",
            "response": {}
        }
        
        # Execute the LangGraph
        result_state = await self.graph.ainvoke(initial_state)
        return result_state.get("response", {})

    async def process_query_stream(self, query: str, context: dict[str, Any] | None = None):
        """
        Process a user query and return an async generator for Server-Sent Events (SSE).
        """
        import json
        logger.info(f"Orchestrator received stream query: {query[:100]}")
        user_id = context.get("user_id", "anonymous") if context else "anonymous"

        initial_state = {
            "query": query,
            "user_id": user_id,
            "agent_used": "",
            "response": {}
        }
        
        # 1. Route the query first
        route_state = await self.route_query(initial_state)
        agent_used = route_state.get("agent_used", "copilot")
        
        # 2. Call the selected agent's stream method
        if agent_used == "copilot" and hasattr(self.copilot, "chat_stream"):
            async for chunk in self.copilot.chat_stream(user_id, query):
                yield chunk
        else:
            # Fallback if streaming is not supported on the target agent (like compliance)
            if agent_used == "compliance":
                res = await self.compliance.chat(user_id, query)
            else:
                res = await self.copilot.chat(user_id, query)
            
            # Send context
            initial_data = {
                "type": "context",
                "context_used": res.get("context_used", []),
                "sources_count": res.get("sources_count", 0)
            }
            yield f"data: {json.dumps(initial_data)}\n\n"
            
            # Send the entire answer as a single chunk
            chunk_data = {"type": "chunk", "content": res.get("answer", "")}
            yield f"data: {json.dumps(chunk_data)}\n\n"
            yield "data: [DONE]\n\n"

