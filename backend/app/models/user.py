"""
OpsPilot — User Model
======================
"""

from typing import Optional
from pydantic import Field
from app.models.base import BaseDocument


class User(BaseDocument):
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: str
    role: str = "engineer"  # admin | engineer | operator | viewer
    is_active: bool = True

    class Settings:
        name = "users"

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
