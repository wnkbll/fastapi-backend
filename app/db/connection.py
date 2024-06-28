import logging

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import get_app_settings, get_app_logger


class DatabaseConnection:
    def __init__(self):
        self.logger: logging.Logger = get_app_logger()
        self.url: PostgresDsn = get_app_settings().database_url
        self.engine: AsyncEngine = create_async_engine(self.url)
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    def get_engine(self) -> AsyncEngine:
        return self.engine

    def get_session(self) -> async_sessionmaker[AsyncSession]:
        return self.session

    async def dispose_engine(self) -> None:
        self.logger.info("Database engine was disposed")
        await self.engine.dispose()
