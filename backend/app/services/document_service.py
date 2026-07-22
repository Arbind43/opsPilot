"""
OpsPilot — Document Service
==============================
Handles document metadata operations and file uploads.
Uses Beanie ODM for MongoDB operations (no SQLAlchemy session needed).
"""

import os
import aiofiles
from typing import List
from uuid import UUID, uuid4
from fastapi import UploadFile

from app.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.utils.file_utils import generate_storage_path, get_file_type, validate_file_extension
from app.core.exceptions import BadRequestError

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./storage/uploads")


class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
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

    async def upload_document(self, file: UploadFile, user_id: UUID, background_tasks: "fastapi.BackgroundTasks", asset_id: UUID | None = None) -> Document:
        """
        Save uploaded file to disk, create database record, and trigger processing.
        """
        import fastapi
        filename = file.filename or "unnamed_file"
        if not validate_file_extension(filename):
            raise BadRequestError(
                message=f"Invalid file type '{os.path.splitext(filename)[1]}'. "
                        f"Allowed: PDF, DOC, DOCX, XLS, XLSX, CSV, TXT, PNG, JPG."
            )

        # Validate max file size
        max_size_bytes = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50")) * 1024 * 1024

        # Save file to disk asynchronously (enforce size limit while streaming)
        file_path = generate_storage_path(UPLOAD_DIR, filename)
        size = 0

        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024 * 1024):  # read in 1 MB chunks
                size += len(content)
                if size > max_size_bytes:
                    # Remove partial file and reject
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass
                    raise BadRequestError(
                        message=f"File exceeds the maximum allowed size of "
                                f"{int(os.getenv('MAX_UPLOAD_SIZE_MB', '50'))} MB."
                    )
                await out_file.write(content)

        # Map file type
        doc_category = get_file_type(filename)

        # Create database record
        doc = Document(
            id=uuid4(),
            title=filename,
            file_path=file_path,
            file_type=file.content_type or "application/octet-stream",
            doc_category=doc_category,
            file_size=size,
            processing_status="pending",
            uploaded_by=user_id,
            asset_id=asset_id,
        )

        saved_doc = await self.repo.create(doc)

        # Trigger background task for AI Pipeline using FastAPI BackgroundTasks
        background_tasks.add_task(self._process_in_background, str(saved_doc.id), saved_doc.file_path)

        return saved_doc

    async def _process_in_background(self, document_id: str, file_path: str):
        import logging
        from ai.pipeline.orchestrator import PipelineOrchestrator
        from app.models.document import Document
        logger = logging.getLogger(__name__)
        try:
            doc = await Document.get(document_id)
            if doc:
                doc.processing_status = "processing"
                await doc.save()

            orchestrator = PipelineOrchestrator()
            await orchestrator.process_document(document_id, file_path)

            doc = await Document.get(document_id)
            if doc:
                doc.processing_status = "completed"
                await doc.save()
        except Exception as e:
            logger.error(f"Background processing failed: {e}")
            doc = await Document.get(document_id)
            if doc:
                doc.processing_status = "failed"
                doc.processing_error = str(e)[:500]
                await doc.save()
