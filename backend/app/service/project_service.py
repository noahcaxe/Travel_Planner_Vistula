import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.travelproject import TravelProject
from app.repository.project_repository import ProjectRepository
from app.db.session import with_session, with_session_readonly
from app.schemas.project import TravelProjectCreate, TravelProjectUpdate


class ProjectService:

    def __init__(self, project_repo: ProjectRepository) -> None:
        self._project_repo = project_repo

    @with_session
    async def create(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        data: TravelProjectCreate,
    ) -> TravelProject:
        return await self._project_repo.create(
            session=session,
            user_id=user_id,
            name=data.name,
            description=data.description,
            start_date=data.start_date,
        )

    @with_session_readonly
    async def get_by_id(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> TravelProject:
        project = await self._project_repo.get_by_id(session, project_id)

        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.user_id != user_id:
            raise PermissionError("Access denied")

        return project

    @with_session_readonly
    async def list_by_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[TravelProject]:
        return await self._project_repo.get_all_by_user(session, user_id)

    @with_session
    async def update(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        data: TravelProjectUpdate,
    ) -> TravelProject:
        project = await self._project_repo.get_by_id(session, project_id)

        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.user_id != user_id:
            raise PermissionError("Access denied")

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        if data.start_date is not None:
            project.start_date = data.start_date

        if data.is_completed is not None:
            project.is_completed = data.is_completed

        return await self._project_repo.update(session, project)

    @with_session
    async def delete(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        project = await self._project_repo.get_by_id(session, project_id)

        if not project:
            raise ValueError(f"Project {project_id} not found")

        if project.user_id != user_id:
            raise PermissionError("Access denied")

        await self._project_repo.delete(session, project)