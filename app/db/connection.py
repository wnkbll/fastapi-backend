from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from pydantic import PostgresDsn
from loguru import logger

from app.core import get_app_settings


class DatabaseConnection:
    def __init__(self):
        self.url: PostgresDsn = get_app_settings().database_url
        self.engine: AsyncEngine = create_async_engine(self.url)
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

    def get_engine(self) -> AsyncEngine:
        return self.engine

    def get_session(self) -> async_sessionmaker[AsyncSession]:
        return self.session

    def dispose_engine(self) -> None:
        logger.info("Database engine was disposed")
        self.engine.dispose()
