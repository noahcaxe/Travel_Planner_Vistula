import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.aic_client import fetch_artwork
from app.model.projectplace import ProjectPlace
from app.repository.project_place_repository import ProjectPlaceRepository
from app.repository.project_repository import ProjectRepository
from app.db.session import with_session, with_session_readonly
from app.schemas.project_place import ProjectPlaceUpdate


class ProjectPlaceService:

    def __init__(
        self,
        place_repo: ProjectPlaceRepository,
        project_repo: ProjectRepository,
    ) -> None:
        self._place_repo = place_repo
        self._project_repo = project_repo

    async def _get_project_or_raise(
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

    @with_session
    async def add_place(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        external_id: int,          
    ) -> ProjectPlace:
        await self._get_project_or_raise(session, project_id, user_id)

       
        existing_places = await self._place_repo.list_by_project(session, project_id)
        if len(existing_places) >= 10:
            raise ValueError("Project cannot have more than 10 places")

        
        existing = await self._place_repo.get_by_external_id(session, project_id, external_id)
        if existing:
            raise ValueError(f"Place {external_id} already exists in this project")

       
        artwork = await fetch_artwork(external_id)
        if artwork is None:
            raise ValueError(f"Artwork {external_id} not found in Art Institute of Chicago")

        return await self._place_repo.create(
            session=session,
            project_id=project_id,
            external_id=external_id,
            title=artwork["title"],
            artist=artwork["artist"],
            image_url=artwork["image_url"],
        )

    @with_session_readonly
    async def get_place(
        self,
        session: AsyncSession,
        place_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ProjectPlace:
        place = await self._place_repo.get_by_id(session, place_id)
        if not place:
            raise ValueError(f"Place {place_id} not found")

        await self._get_project_or_raise(session, place.project_id, user_id)

        return place

    @with_session_readonly
    async def list_places(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> list[ProjectPlace]:
        await self._get_project_or_raise(session, project_id, user_id)
        return await self._place_repo.list_by_project(session, project_id)

    @with_session
    async def update_place(
        self,
        session: AsyncSession,
        place_id: uuid.UUID,
        user_id: uuid.UUID,
        data: ProjectPlaceUpdate,
    ) -> ProjectPlace:
        place = await self._place_repo.get_by_id(session, place_id)
        if not place:
            raise ValueError(f"Place {place_id} not found")

        await self._get_project_or_raise(session, place.project_id, user_id)

        if data.notes is not None:
            place.notes = data.notes

        if data.visited is not None:
            place.visited = data.visited

        return await self._place_repo.update(session, place)

    @with_session
    async def delete_place(
        self,
        session: AsyncSession,
        place_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        place = await self._place_repo.get_by_id(session, place_id)
        if not place:
            raise ValueError(f"Place {place_id} not found")

        await self._get_project_or_raise(session, place.project_id, user_id)

        await self._place_repo.delete(session, place)