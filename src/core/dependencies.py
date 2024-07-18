from typing import Callable, Annotated

from fastapi import Depends

from src.core.config import get_app_settings
from src.core.environments import Environment, EnvironmentTypes
from src.db.connection import get_db_connection
from src.db.repositories.repository import Repository
from src.db.repositories.users import UsersRepository


def get_repository(repository: type[Repository]) -> Callable[[], Repository]:
    def __get_repo() -> Repository:
        db_connection = get_db_connection()
        return repository(db_connection.session_factory)

    return __get_repo


def get_settings() -> Environment:
    return get_app_settings(EnvironmentTypes.dev)


UsersRepositoryDepends = Annotated[UsersRepository, Depends(get_repository(UsersRepository))]

SettingsDepends = Annotated[Environment, Depends(get_settings)]
