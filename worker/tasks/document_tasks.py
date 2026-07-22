"""
OpsPilot — Document Processing Tasks
=======================================
Celery tasks for async document ingestion pipeline.
Uses Beanie (MongoDB) — NOT SQLAlchemy.
"""

from worker.celery_app import celery_app

import asyncio
import logging
from ai.pipeline.orchestrator import PipelineOrchestrator

logger = logging.getLogger(__name__)


async def run_pipeline_async(document_id: str, file_path: str):
    """Run the full AI pipeline asynchronously using Beanie for DB updates."""
    from motor.motor_asyncio import AsyncIOMotorClient
    # Patch for compatibility between Beanie and newer Motor versions
    AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None
    
    from beanie import init_beanie
    import os
    from app.models.document import Document

    # Initialize a fresh Motor + Beanie connection for this Celery worker process
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db = os.getenv("MONGO_DB", "opspilot")

    client = AsyncIOMotorClient(mongo_uri)
    db = client[mongo_db]
    await init_beanie(database=db, document_models=[Document])

    try:
        # Mark as processing
        doc = await Document.get(document_id)
        if doc:
            doc.processing_status = "processing"
            await doc.save()

        # Run AI Orchestrator pipeline
        orchestrator = PipelineOrchestrator()
        result = await orchestrator.process_document(document_id, file_path)

        # Mark as completed
        doc = await Document.get(document_id)
        if doc:
            doc.processing_status = "completed"
            await doc.save()

        logger.info(f"Document {document_id} processed successfully: {result}")
        return result

    except Exception as e:
        logger.error(f"Failed to process document {document_id}: {e}")
        # Mark as failed
        try:
            doc = await Document.get(document_id)
            if doc:
                doc.processing_status = "failed"
                doc.processing_error = str(e)[:500]
                await doc.save()
        except Exception as save_err:
            logger.error(f"Could not update failure status for {document_id}: {save_err}")
        raise e
    finally:
        client.close()


@celery_app.task(name="process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: str, file_path: str):
    """
    Background task to run the AI document processing pipeline.
    Celery tasks are synchronous, so we wrap the async pipeline in asyncio.run().
    """
    return asyncio.run(run_pipeline_async(document_id, file_path))
