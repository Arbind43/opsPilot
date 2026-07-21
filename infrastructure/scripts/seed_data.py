"""
OpsPilot — Seed Data Script
=============================
Populates the database with initial admin user and sample data.
"""

import asyncio
import os
import sys

# Add backend dir to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_factory
from app.core.security import hash_password
from app.models.user import User


async def seed() -> None:
    async with async_session_factory() as session:
        # Check if admin exists
        from app.repositories.user_repo import UserRepository
        repo = UserRepository(session)
        admin = await repo.get_by_email("admin@opspilot.com")
        
        if not admin:
            print("Creating default admin user...")
            admin = User(
                email="admin@opspilot.com",
                hashed_password=hash_password("admin_password"),
                full_name="System Admin",
                role="admin"
            )
            session.add(admin)
            await session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    print("Starting database seed...")
    asyncio.run(seed())
    print("Seed complete.")
