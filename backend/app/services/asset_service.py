"""
OpsPilot — Asset Service
===========================
Asset CRUD, hierarchy management, and timeline aggregation.
"""

from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.asset import Asset
from app.repositories.asset_repo import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate

class AssetService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AssetRepository(session)

    async def get_all_assets(self, offset: int = 0, limit: int = 20) -> List[Asset]:
        return await self.repo.get_all(offset=offset, limit=limit)

    async def get_asset(self, asset_id: UUID) -> Asset | None:
        return await self.repo.get_by_id(asset_id)

    async def create_asset(self, data: AssetCreate) -> Asset:
        asset = Asset(
            name=data.name,
            asset_type=data.asset_type,
            serial_number=data.serial_number,
            location=data.location,
            status=data.status,
            description=data.description,
            metadata_json=data.metadata_json,
            parent_id=data.parent_id
        )
        return await self.repo.create(asset)

    async def update_asset(self, asset_id: UUID, data: AssetUpdate) -> Asset | None:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            return None
        return await self.repo.update(asset, data.model_dump(exclude_unset=True))

    async def delete_asset(self, asset_id: UUID) -> bool:
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            return False
        await self.repo.delete(asset)
        return True

    async def get_asset_tree(self) -> List[Dict[str, Any]]:
        """
        Fetch the entire asset hierarchy as a nested dictionary tree.
        WARNING: This is a simplistic implementation that pulls all assets.
        In a real prod environment with 10k+ assets, this needs optimized CTEs.
        """
        all_assets = await self.repo.get_all(limit=10000)
        
        # Build adjacency list
        asset_map = {}
        for a in all_assets:
            asset_map[a.id] = {
                "id": str(a.id),
                "name": a.name,
                "asset_type": a.asset_type,
                "status": a.status,
                "parent_id": a.parent_id,
                "children": []
            }
            
        # Construct tree
        roots = []
        for a_id, a_dict in asset_map.items():
            parent_id = a_dict["parent_id"]
            if parent_id is None:
                roots.append(a_dict)
            else:
                if parent_id in asset_map:
                    asset_map[parent_id]["children"].append(a_dict)
                else:
                    # Parent not found (e.g. pagination cut off), treat as root
                    roots.append(a_dict)
                    
        return roots

    async def get_timeline(self, asset_id: UUID) -> List[Dict[str, Any]]:
        """Fetch unified timeline (incidents, maintenance, etc.) for a specific asset."""
        # TODO: Pull from Incident, Maintenance, Inspection tables using UNION or individual queries.
        # For now, return empty placeholder.
        return []
