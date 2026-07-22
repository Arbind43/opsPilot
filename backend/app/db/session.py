"""
OpsPilot — MongoDB Async Session
=====================================
Initializes the MongoDB connection using Motor and Beanie.
"""

from motor.motor_asyncio import AsyncIOMotorClient
# Patch for compatibility between Beanie and newer Motor versions
AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None

from beanie import init_beanie
from app.config import get_settings

settings = get_settings()

db_client = None

async def init_db():
    """Initializes the database connection and Beanie ODM."""
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGO_URI)
    db = db_client[settings.MONGO_DB]
    
    # Import models
    from app.models.user import User
    from app.models.asset import Asset
    from app.models.document import Document
    from app.models.incident import Incident
    from app.models.inspection import Inspection
    from app.models.maintenance import MaintenanceRecord
    from app.models.report import Report
    from app.models.conversation import Conversation
    from app.models.audit_log import AuditLog

    await init_beanie(
        database=db,
        document_models=[
            User,
            Asset,
            Document,
            Incident,
            Inspection,
            MaintenanceRecord,
            Report,
            Conversation,
            AuditLog
        ]
    )

async def close_db():
    """Closes the database connection."""
    global db_client
    if db_client:
        db_client.close()

async def get_db_session():
    """Dummy dependency for compatibility during refactor."""
    yield None
