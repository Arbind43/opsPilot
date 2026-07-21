"""OpsPilot — Incident Repository"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.incident import Incident
from app.repositories.base import BaseRepository


class IncidentRepository(BaseRepository[Incident]):
    def __init__(self, session: AsyncSession):
        super().__init__(Incident, session)
