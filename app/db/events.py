from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from loguru import logger

from app.core import get_app_settings


def get_db_engine() -> AsyncEngine:
    database_url = get_app_settings().database_url
    engine: AsyncEngine = create_async_engine(database_url)
    return engine


def get_db_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    return session


async def dispose_db_engine(engine: AsyncEngine) -> None:
    logger.info("Database engine was disposed.")
    await engine.dispose()
