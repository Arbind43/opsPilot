"""
OpsPilot — Document Routes
=============================
Handling document uploads and list operations.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks

from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.core.exceptions import BadRequestError
from app.dependencies import get_current_user_id

import logging
from ai.llm_factory import get_llm
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class KnowledgeGap(BaseModel):
    document_type: str = Field(description="e.g. LOTO Procedure, P&ID Diagram, Incident Report")
    reason: str = Field(description="Why this document is important to have")
    priority: str = Field(description="high, medium, low")


class KnowledgeGapsResponse(BaseModel):
    gaps: List[KnowledgeGap] = Field(description="List of identified missing documents")


router = APIRouter()


@router.get("", response_model=dict, summary="List all documents")
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_current_user_id),
):
    service = DocumentService()
    offset = (page - 1) * page_size
    items = await service.get_all_documents(offset=offset, limit=page_size)
    return {
        "items": [DocumentResponse.model_validate(doc).model_dump(mode="json") for doc in items],
        "page": page,
        "page_size": page_size,
    }


@router.get("/gaps", summary="Detect Knowledge Gaps using AI")
async def get_knowledge_gaps(
    user_id: str = Depends(get_current_user_id),
):
    service = DocumentService()
    # Fetch all documents to see what we have
    items = await service.get_all_documents(offset=0, limit=100)

    # Use doc.title (the correct field name)
    doc_titles = [doc.title for doc in items] if items else []

    llm = get_llm(temperature=0.2)
    structured_llm = llm.with_structured_output(KnowledgeGapsResponse)

    prompt = ChatPromptTemplate.from_template(
        "You are the OpsPilot AI Knowledge Manager. Your job is to analyze the repository of currently uploaded "
        "industrial documents and identify critical missing knowledge.\n\n"
        "Currently uploaded documents:\n{docs}\n\n"
        "Identify 3 standard industrial documents (e.g., LOTO procedures, Maintenance schedules, P&IDs, ISO manuals) "
        "that are missing from this list but should exist in a complete plant repository.\n"
    )

    chain = prompt | structured_llm

    try:
        docs_text = "\n".join(doc_titles) if doc_titles else "No documents uploaded yet."
        result = await chain.ainvoke({"docs": docs_text})
        return result.model_dump()
    except Exception as e:
        logger.error(f"Knowledge gap detection failed: {e}")
        return {
            "gaps": [
                {
                    "document_type": "Emergency Response Plan",
                    "reason": "Crucial for safety compliance and incident handling (AI fallback).",
                    "priority": "high",
                }
            ]
        }


@router.post("/upload", response_model=DocumentResponse, status_code=201, summary="Upload a document")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    asset_id: Optional[UUID] = Form(None),
    user_id: UUID = Depends(get_current_user_id),
):
    service = DocumentService()
    try:
        doc = await service.upload_document(file=file, user_id=user_id, background_tasks=background_tasks, asset_id=asset_id)
        return doc
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{doc_id}", response_model=DocumentResponse, summary="Get document details")
async def get_document(
    doc_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = DocumentService()
    doc = await service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/{doc_id}/retry", response_model=DocumentResponse, summary="Retry processing for a stuck document")
async def retry_document(
    doc_id: UUID,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
):
    service = DocumentService()
    doc = await service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.processing_status == "completed":
        raise HTTPException(status_code=400, detail="Document is already completed")
    # Reset to pending and re-trigger
    from beanie.operators import Set
    from app.models.document import Document
    import uuid
    db_doc = await Document.find_one(Document.id == uuid.UUID(str(doc_id)))
    if db_doc:
        await db_doc.update(Set({"processing_status": "pending", "processing_error": None}))
    background_tasks.add_task(service._process_in_background, str(doc_id), doc.file_path)
    return await service.get_document(doc_id)


@router.delete("/{doc_id}", status_code=204, summary="Delete a document")
async def delete_document(
    doc_id: UUID,
    user_id: str = Depends(get_current_user_id),
):
    service = DocumentService()
    success = await service.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return None
