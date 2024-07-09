from typing import Callable

from src.db.connection import get_db_connection
from src.db.repositories.repository import Repository


def get_repository(repository: type[Repository]) -> Callable[[], Repository]:
    def __get_repo() -> Repository:
        db_connection = get_db_connection()
        return repository(db_connection.session_factory)

    return __get_repo
