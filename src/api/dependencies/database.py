from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.events import get_db_connection
from src.db.repositories.repository import Repository

db_connection = get_db_connection()


def get_repository(repo_type: type[Repository]) -> Callable[[async_sessionmaker[AsyncSession]], Repository]:
    def __get_repo(session: async_sessionmaker[AsyncSession] = Depends(db_connection.session_factory)):
        return repo_type(session)

    return __get_repo
