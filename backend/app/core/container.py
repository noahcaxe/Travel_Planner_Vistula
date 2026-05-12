from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.repository.user_repository import user_repo
from app.repository.token_repository import token_repo
from app.repository.project_repository import project_trav_repo
from app.repository.project_place_repository import proj_place_repo

from app.service.user_service import UserService
from app.service.auth_service import AuthService
from app.service.project_service import ProjectService
from app.service.project_place_service import ProjectPlaceService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.user_service = UserService(
        user_repo=user_repo,
    )

    app.state.auth_service = AuthService(
        user_repo=user_repo,
        token_repo=token_repo,
    )

    app.state.project_service = ProjectService(
        project_repo=project_trav_repo,
    )

    app.state.place_service = ProjectPlaceService(
        place_repo=proj_place_repo,
        project_repo=project_trav_repo,
    )

    yield