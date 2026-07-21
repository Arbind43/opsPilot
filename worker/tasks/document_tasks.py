"""
OpsPilot — Document Processing Tasks
=======================================
Celery tasks for async document ingestion pipeline.
"""

from worker.celery_app import celery_app


import asyncio
import logging
from sqlalchemy import update
from ai.pipeline.orchestrator import PipelineOrchestrator
from app.db.session import async_session_factory, engine
from app.models.document import Document

logger = logging.getLogger(__name__)

async def run_pipeline_async(document_id: str, file_path: str):
    # Dispose of engine connection pool to prevent 'Future attached to a different loop' errors in celery
    await engine.dispose()
    
    try:
        # Mark as processing
        async with async_session_factory() as session:
            await session.execute(
                update(Document)
                .where(Document.id == document_id)
                .values(processing_status="processing")
            )
            await session.commit()

        # Run Orchestrator
        orchestrator = PipelineOrchestrator()
        result = await orchestrator.process_document(document_id, file_path)

        # Mark as completed
        async with async_session_factory() as session:
            await session.execute(
                update(Document)
                .where(Document.id == document_id)
                .values(processing_status="completed")
            )
            await session.commit()
            
        return result

    except Exception as e:
        logger.error(f"Failed to process document {document_id}: {e}")
        # Mark as failed
        async with async_session_factory() as session:
            await session.execute(
                update(Document)
                .where(Document.id == document_id)
                .values(processing_status="failed")
            )
            await session.commit()
        raise e

@celery_app.task(name="process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: str, file_path: str):
    """
    Background task to run the AI document processing pipeline.
    """
    # Celery tasks are synchronous, so we need to run the async pipeline in an event loop
    return asyncio.run(run_pipeline_async(document_id, file_path))
