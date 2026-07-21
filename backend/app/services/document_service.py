"""
OpsPilot — Document Service
==============================
Handles document metadata operations and file uploads.
"""

import os
import aiofiles
from typing import List
from uuid import UUID, uuid4
from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.utils.file_utils import generate_storage_path, get_file_type, validate_file_extension
from app.core.exceptions import BadRequestError

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/data/uploads")

class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DocumentRepository(session)

        # Ensure upload dir exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    async def get_all_documents(self, offset: int = 0, limit: int = 20) -> List[Document]:
        return await self.repo.get_all(offset=offset, limit=limit)

    async def get_document(self, doc_id: UUID) -> Document | None:
        return await self.repo.get_by_id(doc_id)

    async def delete_document(self, doc_id: UUID) -> bool:
        doc = await self.repo.get_by_id(doc_id)
        if not doc:
            return False
        
        # Remove file from disk
        if doc.file_path and os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception:
                pass
                
        await self.repo.delete(doc)
        return True

    async def upload_document(self, file: UploadFile, user_id: UUID, asset_id: UUID | None = None) -> Document:
        """
        Save uploaded file to disk, create database record, and trigger processing.
        """
        if not file.filename or not validate_file_extension(file.filename):
            raise BadRequestError(message="Invalid file type. Allowed: PDF, DOCX, XLSX, Images.")

        # Save file to disk asynchronously
        file_path = generate_storage_path(UPLOAD_DIR, file.filename)
        size = 0
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # read in 1MB chunks
                await out_file.write(content)
                size += len(content)

        # Map file type
        doc_category = get_file_type(file.filename)

        # Create database record
        doc = Document(
            id=uuid4(),
            title=file.filename,
            file_path=file_path,
            file_type=file.content_type or "application/octet-stream",
            doc_category=doc_category,
            file_size=size,
            processing_status="pending",
            uploaded_by=user_id,
            asset_id=asset_id
        )
        
        saved_doc = await self.repo.create(doc)

        # Trigger Celery background task for AI Pipeline
        from worker.tasks.document_tasks import process_document_task
        process_document_task.delay(str(saved_doc.id), saved_doc.file_path)

        return saved_doc
