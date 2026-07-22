"""
OpsPilot — User Repository
=============================
Uses Beanie 2.x query syntax.
"""

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by email address."""
        return await User.find_one({"email": email})
