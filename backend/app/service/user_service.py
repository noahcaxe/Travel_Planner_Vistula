import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.user import User
from app.repository.user_repository import UserRepository
from app.db.session import with_session
from app.core.security import hash_password
from app.schemas.user import UserCreate


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    @with_session
    async def register(
        self,
        session: AsyncSession,
        data: UserCreate,
    ) -> User:
        existing = await self._user_repo.get_by_email(session, data.email)
        if existing:
            raise ValueError(f"User with email '{data.email}' already exists")

        password_hash = hash_password(data.password)

        user = await self._user_repo.create(
            session=session,
            email=data.email,
            password_hash=password_hash,
        )

        return user

    @with_session
    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> User:
        user = await self._user_repo.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user

    @with_session
    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        return await self._user_repo.get_by_email(session, email)

    @with_session
    async def delete(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> None:
        user = await self._user_repo.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        await self._user_repo.delete(session, user)