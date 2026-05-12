from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
import uuid

from app.core.security import decode_access_token
from app.service.user_service import UserService
from app.service.auth_service import AuthService
from app.service.project_service import ProjectService
from app.service.project_place_service import ProjectPlaceService

bearer = HTTPBearer()


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service

def get_auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service

def get_project_service(request: Request) -> ProjectService:
    return request.app.state.project_service

def get_place_service(request: Request) -> ProjectPlaceService:
    return request.app.state.place_service


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> uuid.UUID:
    try:
        payload = decode_access_token(credentials.credentials)
        return uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")