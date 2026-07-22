"""
OpsPilot — Auth Routes
========================
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshRequest,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.core.exceptions import BadRequestError
from app.dependencies import get_current_user_id

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: RegisterRequest,
    settings: Settings = Depends(get_settings),
):
    """Register a new user account."""
    service = AuthService(settings)
    user = await service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    settings: Settings = Depends(get_settings),
):
    """Authenticate and receive JWT tokens."""
    service = AuthService(settings)
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    settings: Settings = Depends(get_settings),
):
    """Refresh an expired access token."""
    service = AuthService(settings)
    return await service.refresh_tokens(data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: str = Depends(get_current_user_id),
):
    """Get the current authenticated user's profile."""
    from app.repositories.user_repo import UserRepository
    repo = UserRepository()
    user = await repo.get_by_id(user_id)
    return user


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    settings: Settings = Depends(get_settings),
):
    """Request a password reset OTP.
    In demo mode, the OTP is returned directly.
    In production, this would be sent via email.
    """
    service = AuthService(settings)
    otp = await service.request_password_reset(data.email)
    return {
        "message": "If this email is registered, a reset code has been generated.",
        "demo_otp": otp,  # Remove in production — only for demo
    }


@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    settings: Settings = Depends(get_settings),
):
    """Verify OTP and set a new password."""
    service = AuthService(settings)
    try:
        await service.reset_password(data.email, data.otp, data.new_password)
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return {"message": "Password reset successfully. You can now log in."}
