"""
OpsPilot — Copilot API Routes
================================
Endpoints for the AI Copilot chat interface.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.dependencies import get_current_user_id

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    context_used: List[Dict[str, Any]]


def _get_orchestrator():
    """Lazy-load the orchestrator so import errors don't crash the entire app."""
    from ai.agents.orchestrator import AgentOrchestrator
    return AgentOrchestrator()


@router.post("/chat", response_model=ChatResponse, summary="Chat with OpsPilot AI")
async def chat_with_copilot(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
):
    try:
        orchestrator = _get_orchestrator()
        response = await orchestrator.process_query(
            query=request.query,
            context={"user_id": user_id},
        )
        return ChatResponse(
            answer=response.get("answer", ""),
            context_used=response.get("context_used", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream", summary="Stream Chat with OpsPilot AI")
async def chat_with_copilot_stream(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
):
    try:
        orchestrator = _get_orchestrator()
        generator = orchestrator.process_query_stream(
            query=request.query,
            context={"user_id": user_id},
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
