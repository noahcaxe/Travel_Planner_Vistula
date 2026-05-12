import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.projectplace import ProjectPlace


class ProjectPlaceRepository:

    async def create(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        external_id: uuid.UUID,
        title: str,
        artist: str | None,
        image_url: str | None,
    ) -> ProjectPlace:
        place = ProjectPlace(
            project_id=project_id,
            external_id=external_id,
            title=title,
            artist=artist,
            image_url=image_url,
        )

        session.add(place)
        await session.flush()
        await session.refresh(place)

        return place

    async def get_by_id(
        self,
        session: AsyncSession,
        place_id: uuid.UUID,
    ) -> ProjectPlace | None:
        result = await session.execute(
            select(ProjectPlace).where(ProjectPlace.id == place_id)
        )
        return result.scalar_one_or_none()

    async def get_by_external_id(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
        external_id: int,         
    ) -> ProjectPlace | None:
        result = await session.execute(
            select(ProjectPlace).where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.external_id == external_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_project(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
    ) -> list[ProjectPlace]:
        result = await session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id)
        )
        return list(result.scalars().all())

    async def update(
        self,
        session: AsyncSession,
        place: ProjectPlace,
    ) -> ProjectPlace:
        session.add(place)
        await session.flush()
        await session.refresh(place)

        return place

    async def delete(
        self,
        session: AsyncSession,
        place: ProjectPlace,
    ) -> None:
        await session.delete(place)
        await session.flush()


proj_place_repo = ProjectPlaceRepository()