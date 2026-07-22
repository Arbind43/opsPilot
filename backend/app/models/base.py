"""
OpsPilot — Base Model
======================
Base document with shared audit columns for Beanie.
"""

from datetime import datetime, timezone
import uuid
from pydantic import Field
from beanie import Document, Insert, Replace, before_event

class BaseDocument(Document):
    """Base document class with UUID primary key and timestamps."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at

    @before_event(Replace)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
