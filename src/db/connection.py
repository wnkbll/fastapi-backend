from functools import lru_cache

from loguru import logger
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import get_app_settings
from src.core.environments import Environment, EnvironmentTypes
from src.models.tables import Table


class DatabaseConnection:
    def __init__(self, settings: Environment):
        self._env_type: EnvironmentTypes = settings.env_type
        self._url: PostgresDsn = (
            settings.database.test_url if self._env_type == EnvironmentTypes.test else settings.database.url
        )
        self._engine: AsyncEngine = create_async_engine(self.url)
        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    @property
    def url(self) -> PostgresDsn:
        return self._url

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def init_db(self) -> None:
        async with self.engine.begin() as connection:
            if self._env_type == EnvironmentTypes.test:
                await connection.run_sync(Table.metadata.drop_all)
            await connection.run_sync(Table.metadata.create_all)
            logger.info("Database was initialized")

    async def dispose_engine(self) -> None:
        await self.engine.dispose()
        logger.info("Engine was disposed")


@lru_cache
def get_db_connection(env_type: EnvironmentTypes):
    settings = get_app_settings(env_type)
    db_connection = DatabaseConnection(settings)
    return db_connection
