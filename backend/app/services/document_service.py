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
        import uuid as _uuid
        from ai.pipeline.orchestrator import PipelineOrchestrator
        from app.models.document import Document
        _logger = logging.getLogger(__name__)

        doc_uuid = _uuid.UUID(document_id)

        async def _set_status(status: str, error: str | None = None):
            """Update document status using correct Beanie raw-dict $set syntax."""
            try:
                update_data: dict = {"processing_status": status}
                if error:
                    update_data["processing_error"] = error[:500]
                # Use raw MongoDB $set — works reliably on both instance and query
                await Document.find_one(Document.id == doc_uuid).update(
                    {"$set": update_data}
                )
                _logger.info(f"Document {document_id} status -> {status}")
            except Exception as upd_err:
                _logger.error(f"Status update failed for {document_id}: {upd_err}")

        try:
            await _set_status("processing")

            # Guard: file might not exist on cloud (ephemeral storage)
            if not os.path.exists(file_path):
                raise FileNotFoundError(
                    f"Uploaded file missing at '{file_path}'. "
                    "Cloud storage may be ephemeral — please re-upload the document."
                )

            orchestrator = PipelineOrchestrator()
            await orchestrator.process_document(document_id, file_path)
            await _set_status("completed")

        except Exception as e:
            _logger.error(f"Background processing failed for {document_id}: {e}")
            await _set_status("failed", str(e))

