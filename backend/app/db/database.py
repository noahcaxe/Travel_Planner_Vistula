from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config.config import settings

Base = declarative_base()


engine = create_async_engine(
    settings.DATABASE_URL,
    echo = False,
    future = True,
    pool_size = 5,
    max_overflow = 10,
)


AsyncSessionFactory = async_sessionmaker(
    bind = engine,
    expire_on_commit= False,
    autoflush= False,
    autocommit = False,
    class_ = AsyncSession,
)

async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session: 
        yield session
