"""
OpsPilot — Auth Service
=========================
Handles user registration, login, and token management.
Business logic only — no HTTP concerns.
"""

import random
import string
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.core.exceptions import AlreadyExistsError, AuthenticationError, BadRequestError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

logger = structlog.get_logger()


class AuthService:
    """Orchestrates authentication business logic."""

    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.repo = UserRepository(session)
        self.settings = settings

    async def register(self, data: RegisterRequest) -> User:
        """Register a new user. Raises AlreadyExistsError if email taken."""
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise AlreadyExistsError("User", "email", data.email)

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        return await self.repo.create(user)

    async def login(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user and return JWT tokens."""
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        return TokenResponse(
            access_token=create_access_token(token_data, self.settings),
            refresh_token=create_refresh_token(token_data, self.settings),
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Issue new tokens from a valid refresh token."""
        payload = decode_refresh_token(refresh_token, self.settings)
        user = await self.repo.get_by_id(payload["sub"])
        if not user or not user.is_active:
            raise AuthenticationError("Invalid refresh token")

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        return TokenResponse(
            access_token=create_access_token(token_data, self.settings),
            refresh_token=create_refresh_token(token_data, self.settings),
        )

    async def request_password_reset(self, email: str) -> str:
        """Generate a 6-digit OTP and store in Redis for 15 minutes.
        Returns the OTP (demo mode — in production this would be emailed)."""
        import redis
        user = await self.repo.get_by_email(email)
        # Always return success to avoid email enumeration
        if not user:
            return "000000"  # silent fail, user doesn't exist

        otp = "".join(random.choices(string.digits, k=6))
        r = redis.Redis.from_url(self.settings.REDIS_URL, decode_responses=True)
        r.setex(f"pwd_reset:{email}", 900, otp)  # 15 min TTL
        logger.info("password_reset_otp_generated", email=email)
        return otp

    async def reset_password(self, email: str, otp: str, new_password: str) -> None:
        """Verify the OTP and update the user's password."""
        import redis
        r = redis.Redis.from_url(self.settings.REDIS_URL, decode_responses=True)
        stored_otp = r.get(f"pwd_reset:{email}")

        if not stored_otp or stored_otp != otp:
            raise BadRequestError("Invalid or expired reset code")

        user = await self.repo.get_by_email(email)
        if not user:
            raise AuthenticationError("User not found")

        user.hashed_password = hash_password(new_password)
        await self.session.commit()
        r.delete(f"pwd_reset:{email}")
        logger.info("password_reset_complete", email=email)
