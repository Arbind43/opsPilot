"""
OpsPilot — Text Chunker
==========================
Slices parsed text into semantic, overlapping chunks.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Takes the parsed document (with sections) and breaks it into chunks.
        Metadata is attached to each chunk (e.g. section header, doc title).
        """
        chunks = []
        doc_title = parsed_doc.get("title", "Unknown")
        sections = parsed_doc.get("sections", [])

        if not sections:
            # Fallback if no sections were parsed
            content = parsed_doc.get("content", "")
            raw_chunks = self._sliding_window(content)
            for i, text in enumerate(raw_chunks):
                chunks.append({
                    "id": f"chunk_{i}",
                    "text": text,
                    "metadata": {
                        "document_title": doc_title,
                        "section": "Main"
                    }
                })
            return chunks

        # Chunk section by section to preserve logical boundaries
        chunk_idx = 0
        for section in sections:
            header = section.get("header", "Unknown Section")
            content = section.get("content", "")
            
            if not content:
                continue
                
            raw_chunks = self._sliding_window(content)
            for text in raw_chunks:
                chunks.append({
                    "id": f"chunk_{chunk_idx}",
                    "text": text,
                    "metadata": {
                        "document_title": doc_title,
                        "section": header
                    }
                })
                chunk_idx += 1

        logger.info(f"Generated {len(chunks)} chunks for document.")
        return chunks

    def _sliding_window(self, text: str) -> List[str]:
        """
        Basic character-level sliding window chunker.
        In production, a token-based chunker (like RecursiveCharacterTextSplitter from LangChain) is preferred.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            # Advance start by chunk_size - overlap
            start += (self.chunk_size - self.chunk_overlap)
            
        return chunks
