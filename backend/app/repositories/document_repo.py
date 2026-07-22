"""
OpsPilot — Document Repository
=================================
"""


from app.models.document import Document, DocumentChunk
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    def __init__(self):
        super().__init__(DocumentChunk)
