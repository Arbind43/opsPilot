"""
OpsPilot — Document & DocumentChunk Models
============================================
"""

from typing import Optional, Dict, Any
import uuid
from pydantic import Field
from app.models.base import BaseDocument

class Document(BaseDocument):
    title: str = Field(index=True)
    file_path: str
    file_type: str  # pdf | docx | xlsx | image
    doc_category: Optional[str] = None
    file_size: int = 0
    processing_status: str = "pending"  # pending | processing | completed | failed
    processing_error: Optional[str] = None
    extracted_text: Optional[str] = None
    extracted_metadata: Optional[Dict[str, Any]] = None
    version: int = 1

    uploaded_by: uuid.UUID
    asset_id: Optional[uuid.UUID] = None

    class Settings:
        name = "documents"

    def __repr__(self) -> str:
        return f"<Document {self.title} ({self.processing_status})>"


class DocumentChunk(BaseDocument):
    document_id: uuid.UUID = Field(index=True)
    chunk_index: int
    content: str
    chroma_id: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

    class Settings:
        name = "document_chunks"

    def __repr__(self) -> str:
        return f"<DocumentChunk doc={self.document_id} idx={self.chunk_index}>"
