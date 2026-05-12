import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.model.travelproject import TravelProject


class ProjectRepository:

    async def create(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        name: str,
        description: str | None,
        start_date: date | None,
    ) -> TravelProject:

        project = TravelProject(
            user_id=user_id,
            name=name,
            description=description,
            start_date=start_date,
        )

        session.add(project)

        await session.flush()

        result = await session.execute(
            select(TravelProject)
            .where(TravelProject.id == project.id)
            .options(selectinload(TravelProject.places))
        )

        return result.scalar_one()

    async def get_by_id(
        self,
        session: AsyncSession,
        project_id: uuid.UUID,
    ) -> TravelProject | None:

        result = await session.execute(
            select(TravelProject)
            .where(TravelProject.id == project_id)
            .options(selectinload(TravelProject.places))
        )

        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[TravelProject]:

        result = await session.execute(
            select(TravelProject)
            .where(TravelProject.user_id == user_id)
            .options(selectinload(TravelProject.places))
            .order_by(TravelProject.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        session: AsyncSession,
        project: TravelProject,
    ) -> TravelProject:

        session.add(project)

        await session.flush()

        result = await session.execute(
            select(TravelProject)
            .where(TravelProject.id == project.id)
            .options(selectinload(TravelProject.places))
        )

        return result.scalar_one()

    async def delete(
        self,
        session: AsyncSession,
        project: TravelProject,
    ) -> None:

        await session.delete(project)

        await session.flush()


project_trav_repo = ProjectRepository()