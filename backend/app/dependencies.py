"""
OpsPilot — FastAPI Dependencies
================================
Dependency injection functions used across API routes.
"""

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repo import UserRepository

# Bearer token scheme
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> str:
    """Extract and validate the current user ID from the JWT bearer token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials, settings)
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id)
) -> User:
    """Return the full User model for the authenticated user."""
    repo = UserRepository()
    user = await repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def require_role(allowed_roles: list[str]):
    """Dependency factory that checks if the current user has one of the allowed roles."""

    async def _check_role(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
        settings: Settings = Depends(get_settings),
    ) -> dict:
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        payload = decode_access_token(credentials.credentials, settings)
        role = payload.get("role", "")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return payload

    return _check_role
