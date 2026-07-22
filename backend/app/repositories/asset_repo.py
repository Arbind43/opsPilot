"""
OpsPilot — Asset Repository
==============================
"""

from typing import List
from uuid import UUID


from app.models.asset import Asset
from app.repositories.base import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    def __init__(self):
        super().__init__(Asset)

    async def get_root_assets(self) -> List[Asset]:
        """Get all top-level assets (no parent)."""
        return await Asset.find({"parent_id": None}).to_list()

    async def get_children(self, parent_id: UUID) -> List[Asset]:
        """Get all direct children of an asset."""
        return await Asset.find({"parent_id": parent_id}).to_list()
