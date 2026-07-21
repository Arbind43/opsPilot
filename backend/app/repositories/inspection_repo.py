"""OpsPilot — Inspection Repository"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.inspection import Inspection
from app.repositories.base import BaseRepository


class InspectionRepository(BaseRepository[Inspection]):
    def __init__(self, session: AsyncSession):
        super().__init__(Inspection, session)
