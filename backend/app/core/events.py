"""
OpsPilot — Application Lifecycle Events
=========================================
Startup and shutdown hooks for initializing and tearing down resources.
"""

import os

import structlog

from app.config import get_settings
from app.core.logging import setup_logging
from app.db.session import init_db, close_db
from app.db.neo4j_client import neo4j_client
from app.db.pinecone_client import pinecone_client

logger = structlog.get_logger()


async def on_startup() -> None:
    """Called when the application starts."""
    settings = get_settings()

    # Configure structured logging
    setup_logging(settings.LOG_LEVEL)

    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Initialize database connections
    logger.info("startup", app=settings.APP_NAME, env=settings.APP_ENV)

    # Initialize Beanie & MongoDB
    try:
        await init_db()
        logger.info("mongodb_connected")
    except Exception as e:
        logger.exception("mongodb_connection_failed", error=str(e))

    # Verify Neo4j connection
    try:
        await neo4j_client.verify_connectivity()
        logger.info("neo4j_connected")
    except Exception as e:
        logger.warning("neo4j_connection_failed", error=str(e))

    # 2. Check Pinecone connection
    try:
        pinecone_client.heartbeat()
        logger.info("pinecone_connected")
    except Exception as e:
        logger.warning("pinecone_connection_failed", error=str(e))

    logger.info("startup_complete")

    # Recover any documents that were stuck in 'processing' due to a server crash
    try:
        from app.models.document import Document
        from beanie.operators import Set
        stuck = await Document.find(Document.processing_status == "processing").to_list()
        if stuck:
            logger.warning("recovering_stuck_documents", count=len(stuck))
            for doc in stuck:
                await doc.update(Set({"processing_status": "pending"}))
            # Re-trigger processing for recovered docs in the background
            import asyncio
            from ai.pipeline.orchestrator import PipelineOrchestrator
            async def _retry(doc_id, file_path):
                from beanie.operators import Set as _Set
                from app.models.document import Document as _Doc
                import uuid as _uuid
                try:
                    await _Doc.find_one(_Doc.id == _uuid.UUID(doc_id)).update(_Set({"processing_status": "processing"}))
                    await PipelineOrchestrator().process_document(doc_id, file_path)
                    await _Doc.find_one(_Doc.id == _uuid.UUID(doc_id)).update(_Set({"processing_status": "completed"}))
                except Exception as ex:
                    logger.error("recovery_failed", doc_id=doc_id, error=str(ex))
                    await _Doc.find_one(_Doc.id == _uuid.UUID(doc_id)).update(_Set({"processing_status": "failed", "processing_error": str(ex)[:500]}))
            for doc in stuck:
                asyncio.ensure_future(_retry(str(doc.id), doc.file_path))
    except Exception as e:
        logger.warning("startup_recovery_failed", error=str(e))


async def on_shutdown() -> None:
    """Called when the application shuts down."""
    logger.info("shutdown_started")

    # Close MongoDB connection
    await close_db()

    # Close Neo4j driver
    await neo4j_client.close()

    logger.info("shutdown_complete")
