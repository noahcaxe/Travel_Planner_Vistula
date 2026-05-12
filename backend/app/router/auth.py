from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_auth_service, get_user_service
from app.schemas.auth_schema import LoginRequest, RefreshRequest, TokenPair
from app.schemas.user import UserCreate, UserResponse
from app.service.auth_service import AuthService
from app.service.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=TokenPair)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return await auth_service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return await auth_service.refresh(data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout", status_code=204)
async def logout(
    data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout(data.refresh_token)