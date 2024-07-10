from typing import Callable, Annotated

from fastapi import Depends

from src.db.connection import get_db_connection
from src.db.repositories.articles import ArticlesRepository
from src.db.repositories.repository import Repository
from src.db.repositories.users import UsersRepository


def get_repository(repository: type[Repository]) -> Callable[[], Repository]:
    def __get_repo() -> Repository:
        db_connection = get_db_connection()
        return repository(db_connection.session_factory)

    return __get_repo


UsersRepositoryDepends = Annotated[Repository, Depends(get_repository(UsersRepository))]
ArticlesRepositoryDepends = Annotated[Repository, Depends(get_repository(ArticlesRepository))]
