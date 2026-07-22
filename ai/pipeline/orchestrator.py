"""
OpsPilot — Pipeline Orchestrator
===================================
Coordinates the full document processing pipeline:
Upload → OCR → Layout Parsing → Entity Extraction → Chunking → Embedding → Graph Update
"""

import asyncio
import structlog
from typing import Any
from concurrent.futures import ThreadPoolExecutor

logger = structlog.get_logger()
_thread_pool = ThreadPoolExecutor(max_workers=4)


class PipelineOrchestrator:
    """
    Orchestrates the entire document ingestion pipeline.
    Each step is modular and can be run independently.
    """

    def __init__(self) -> None:
        from ai.pipeline.ocr import OCREngine
        from ai.pipeline.parser import DocumentParser
        from ai.pipeline.extractor import KnowledgeExtractor
        from ai.pipeline.chunker import TextChunker
        from ai.pipeline.embedder import VectorEmbedder
        from ai.graph.builder import GraphBuilder
        
        self._ocr = OCREngine()
        self._parser = DocumentParser()
        self._extractor = KnowledgeExtractor()
        self._chunker = TextChunker()
        self._embedder = VectorEmbedder()
        self._graph_builder = GraphBuilder()

    async def process_document(self, document_id: str, file_path: str) -> dict[str, Any]:
        """
        Run the full pipeline on a document.
        """
        logger.info("pipeline_start", document_id=document_id)

        # Step 1: OCR / Text Extraction (run in thread so it doesn't block event loop)
        logger.info("pipeline_ocr_start", document_id=document_id)
        loop = asyncio.get_event_loop()
        raw_text = await loop.run_in_executor(_thread_pool, self._ocr.extract_text, file_path, "")
        logger.info("pipeline_ocr_complete", document_id=document_id, chars=len(raw_text))

        # Step 2: Layout Parsing (fast, CPU-bound — also off the event loop)
        logger.info("pipeline_parsing_start", document_id=document_id)
        parsed_doc = await loop.run_in_executor(_thread_pool, self._parser.parse, raw_text)
        parsed_sections = parsed_doc.get("sections", [])
        logger.info("pipeline_parsing_complete", document_id=document_id, sections=len(parsed_sections))

        # Step 3: Entity & Relation Extraction — call async directly, no thread overhead
        logger.info("pipeline_extraction_start", document_id=document_id)
        graph_data = await self._extractor._extract_async(parsed_doc)
        entities = graph_data.get("entities", [])
        relations = graph_data.get("relations", [])
        logger.info("pipeline_extraction_complete", entities=len(entities), relations=len(relations))

        # Step 4: Chunking
        logger.info("pipeline_chunking_start", document_id=document_id)
        chunks = self._chunker.chunk_document(parsed_doc)
        logger.info("pipeline_chunking_complete", document_id=document_id, chunks=len(chunks))

        # Step 5: Embedding + Vector Storage
        logger.info("pipeline_embedding_start", document_id=document_id)
        embed_success = await self._embedder.embed_and_store(chunks, document_id)
        logger.info("pipeline_embedding_complete", document_id=document_id, success=embed_success)

        # Step 6: Graph Update
        logger.info("pipeline_graph_start", document_id=document_id)
        graph_success = await self._graph_builder.update_graph(graph_data, document_id)
        logger.info("pipeline_graph_complete", document_id=document_id, success=graph_success)

        logger.info("pipeline_complete", document_id=document_id)
        return {
            "document_id": document_id,
            "text_length": len(raw_text),
            "entities_count": len(entities),
            "relations_count": len(relations),
            "chunks_count": len(chunks),
        }
