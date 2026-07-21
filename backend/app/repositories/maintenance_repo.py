"""OpsPilot — Maintenance Repository"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.maintenance import MaintenanceRecord
from app.repositories.base import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(MaintenanceRecord, session)
