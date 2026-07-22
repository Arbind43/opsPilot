"""OpsPilot — Report Repository"""

from app.models.report import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)
