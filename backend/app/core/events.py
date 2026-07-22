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


async def on_shutdown() -> None:
    """Called when the application shuts down."""
    logger.info("shutdown_started")

    # Close MongoDB connection
    await close_db()

    # Close Neo4j driver
    await neo4j_client.close()

    logger.info("shutdown_complete")
