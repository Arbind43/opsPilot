"""
OpsPilot — Service Stubs
===========================
Placeholder services to be implemented per module.
Each service follows the pattern: Service(session) → repo → DB
"""

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()


class UserService:
    """User management operations (CRUD, role changes)."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 14 (Settings)


class AssetService:
    """Asset CRUD, hierarchy management, and timeline aggregation."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 2 (Dashboard) / Module 6 (Knowledge Graph)


class DocumentService:
    """Document upload metadata management and status tracking."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 3 (Document Upload)


class UploadService:
    """File upload handling: validation, storage, and pipeline triggering."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 3 (Document Upload)


class DashboardService:
    """Aggregates statistics, activity feed, and alerts for the dashboard."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 2 (Dashboard)


class ReportService:
    """Report generation, listing, and PDF export."""
    def __init__(self, session: AsyncSession):
        self.session = session
        # TODO: Implement in Module 13 (Reports)
