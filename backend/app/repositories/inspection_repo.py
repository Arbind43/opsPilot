"""OpsPilot — Inspection Repository"""

from app.models.inspection import Inspection
from app.repositories.base import BaseRepository


class InspectionRepository(BaseRepository[Inspection]):
    def __init__(self):
        super().__init__(Inspection)
