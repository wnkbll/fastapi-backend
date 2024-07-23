from typing import Callable, Annotated

from fastapi import Depends

from depricated.src.core import get_app_settings
from depricated.src.core import Environment, EnvironmentTypes
from depricated.src.db import get_postgres_connection
from depricated.src.db.repositories.repository import Repository
from depricated.src.db import TasksRepository
from depricated.src.db import UsersRepository


def get_repository(repository: type[Repository]) -> Callable[[], Repository]:
    def __get_repo() -> Repository:
        db_connection = get_postgres_connection()
        return repository(db_connection.session_factory)

    return __get_repo


def get_settings() -> Environment:
    return get_app_settings(EnvironmentTypes.dev)


UsersRepositoryDepends = Annotated[UsersRepository, Depends(get_repository(UsersRepository))]
TasksRepositoryDepends = Annotated[TasksRepository, Depends(get_repository(TasksRepository))]

SettingsDepends = Annotated[Environment, Depends(get_settings)]
