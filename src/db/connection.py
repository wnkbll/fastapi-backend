import logging

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import get_app_settings, get_app_logger


class DatabaseConnection:
    def __init__(self):
        self._logger: logging.Logger = get_app_logger()
        self._url: PostgresDsn = get_app_settings().database_url
        self._engine: AsyncEngine = create_async_engine(self._url)
        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def dispose_engine(self) -> None:
        self._logger.info("Database engine was disposed")
        await self.engine.dispose()
