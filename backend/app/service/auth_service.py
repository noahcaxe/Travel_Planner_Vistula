import uuid
import hashlib
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.user import User
from app.model.token import RefreshToken
from app.repository.user_repository import UserRepository
from app.repository.token_repository import TokenRepository
from app.db.session import with_session
from app.core.security import verify_password, create_access_token, create_refresh_token


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: TokenRepository,
    ) -> None:
        self._user_repo = user_repo
        self._token_repo = token_repo

    @with_session
    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> dict:
        user = await self._user_repo.get_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        access_token = create_access_token({"sub": str(user.id)})
        raw_refresh, expires_at = create_refresh_token()

        token_hash = hashlib.sha256(raw_refresh.encode()).hexdigest()

        await self._token_repo.create(
            session=session,
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh,
            "token_type": "bearer",
        }

    @with_session
    async def refresh(
        self,
        session: AsyncSession,
        raw_refresh_token: str,
    ) -> dict:

        token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()

        token: RefreshToken | None = await self._token_repo.get_by_hash(
            session, token_hash
        )

        if not token:
            raise ValueError("Refresh token not found")

        if token.revoked:
            raise ValueError("Refresh token has been revoked")

        now = datetime.now(timezone.utc)
        if token.expires_at.replace(tzinfo=timezone.utc) < now:
            raise ValueError("Refresh token has expired")

      
        await self._token_repo.revoke(session, token)

        access_token = create_access_token({"sub": str(token.user_id)})
        raw_new_refresh, new_expires_at = create_refresh_token()
        new_hash = hashlib.sha256(raw_new_refresh.encode()).hexdigest()

        await self._token_repo.create(
            session=session,
            user_id=token.user_id,
            token_hash=new_hash,
            expires_at=new_expires_at,
        )

        return {
            "access_token": access_token,
            "refresh_token": raw_new_refresh,
            "token_type": "bearer",
        }

    @with_session
    async def logout(
        self,
        session: AsyncSession,
        raw_refresh_token: str,
    ) -> None:
        token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()
        token = await self._token_repo.get_by_hash(session, token_hash)
        if token and not token.revoked:
            await self._token_repo.revoke(session, token)

    @with_session
    async def revoke_all_for_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> None:
        await self._token_repo.revoke_all_by_user(session, user_id)