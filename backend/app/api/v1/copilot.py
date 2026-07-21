"""
OpsPilot — Copilot API Routes
================================
Endpoints for the AI Copilot chat interface.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user_id, get_db
from ai.agents.orchestrator import AgentOrchestrator

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    context_used: List[Dict[str, Any]]

# We instantiate the orchestrator once for the router
orchestrator = AgentOrchestrator()

from fastapi.responses import StreamingResponse

@router.post("/chat", response_model=ChatResponse, summary="Chat with OpsPilot AI")
async def chat_with_copilot(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    try:
        response = await orchestrator.process_query(
            query=request.query,
            context={"user_id": user_id}
        )
        return ChatResponse(
            answer=response.get("answer", ""),
            context_used=response.get("context_used", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream", summary="Stream Chat with OpsPilot AI")
async def chat_with_copilot_stream(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    try:
        generator = orchestrator.process_query_stream(
            query=request.query,
            context={"user_id": user_id}
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
