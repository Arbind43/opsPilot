"""OpsPilot — Maintenance Repository"""

from app.models.maintenance import MaintenanceRecord
from app.repositories.base import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceRecord]):
    def __init__(self):
        super().__init__(MaintenanceRecord)
