"""
OpsPilot — Asset Repository
==============================
"""

from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.repositories.base import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    def __init__(self, session: AsyncSession):
        super().__init__(Asset, session)

    async def get_root_assets(self) -> List[Asset]:
        """Get all top-level assets (no parent)."""
        result = await self.session.execute(
            select(Asset).where(Asset.parent_id.is_(None))
        )
        return list(result.scalars().all())

    async def get_children(self, parent_id: UUID) -> List[Asset]:
        """Get all direct children of an asset."""
        result = await self.session.execute(
            select(Asset).where(Asset.parent_id == parent_id)
        )
        return list(result.scalars().all())
