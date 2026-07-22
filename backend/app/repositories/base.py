"""
OpsPilot — Base Repository
=============================
Generic CRUD repository pattern for Beanie documents.
"""

from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID

from app.models.base import BaseDocument

ModelType = TypeVar("ModelType", bound=BaseDocument)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD operations for any Beanie model."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, id: UUID) -> ModelType | None:
        """Fetch a single record by primary key."""
        return await self.model.get(id)

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> List[ModelType]:
        """Fetch multiple records with optional filtering and pagination."""
        query = self.model.find()
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.find({key: value})
        return await query.skip(offset).limit(limit).to_list()

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count records with optional filtering."""
        query = self.model.find()
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.find({key: value})
        return await query.count()

    async def create(self, obj: ModelType) -> ModelType:
        """Insert a new record."""
        return await obj.insert()

    async def update(self, obj: ModelType, data: dict[str, Any]) -> ModelType:
        """Update an existing record with the given data dict."""
        update_query = {"$set": {}}
        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                update_query["$set"][key] = value
        if update_query["$set"]:
            await obj.update(update_query)
        return obj

    async def delete(self, obj: ModelType) -> None:
        """Delete a record."""
        await obj.delete()
