from functools import wraps
from app.db.database import AsyncSessionFactory
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession

_current_session: ContextVar[AsyncSession] = ContextVar("current_session", default=None)

def with_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session = _current_session.get()
        if session:
            return await func(self, session, *args, **kwargs)

 
        async with AsyncSessionFactory() as session:
            token = _current_session.set(session)
            try:
                result = await func(self, session, *args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                _current_session.reset(token)

    return wrapper



def with_session_readonly(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session = _current_session.get()
        if session:
            return await func(self, session, *args, **kwargs)

        async with AsyncSessionFactory() as session:
            token = _current_session.set(session)
            try:
                result = await func(self, session, *args, **kwargs)
                return result
            except Exception:
                raise
            finally:
                _current_session.reset(token)

            
    return wrapper

def with_session_func(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = _current_session.get()

        if session:
            return await func(session, *args, **kwargs)

        async with AsyncSessionFactory() as session:
            token = _current_session.set(session)
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                _current_session.reset(token)

    return wrapper
