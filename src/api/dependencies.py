from typing import Callable, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.core.config import get_app_settings
from src.core.settings import Settings
from src.db.db_postgres import get_async_engine
from src.db.repositories.repository import Repository
from src.db.repositories.tasks import TasksRepository
from src.db.repositories.users import UsersRepository


def get_async_session_factory():
    async_engine: AsyncEngine = get_async_engine()

    async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=async_engine, autoflush=False, expire_on_commit=False
    )

    return async_session_factory


def get_repository(repository: type[Repository]) -> Callable[[async_sessionmaker[AsyncSession]], Repository]:
    def __get_repo(
            async_session_factory: async_sessionmaker[AsyncSession] = Depends(get_async_session_factory)
    ) -> Repository:
        return repository(async_session_factory)

    return __get_repo


UsersRepositoryDepends = Annotated[UsersRepository, Depends(get_repository(UsersRepository))]
TasksRepositoryDepends = Annotated[TasksRepository, Depends(get_repository(TasksRepository))]

SettingsDepends = Annotated[Settings, Depends(get_app_settings)]
