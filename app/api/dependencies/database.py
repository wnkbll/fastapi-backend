from typing import Callable
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db import DatabaseConnection
from app.db.repositories import Repository

db_connection = DatabaseConnection()


def get_repository(repo_type: type[Repository[DeclarativeBase]]) -> Callable[[async_sessionmaker[AsyncSession]], Repository]:
    def __get_repo(session: async_sessionmaker[AsyncSession] = Depends(db_connection.get_session)):
        return repo_type(session)

    return __get_repo
