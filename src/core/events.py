from typing import Callable

from src.core.environments import Environment
from src.db.connection import get_db_connection
from src.models.tables import Table


def create_start_app_handler(settings: Environment) -> Callable:
    async def start_app():
        db_connection = get_db_connection(settings.env_type)
        await db_connection.init_db(Table)

    return start_app


def create_stop_app_handler(settings: Environment) -> Callable:
    async def stop_app() -> None:
        db_connection = get_db_connection(settings.env_type)
        await db_connection.dispose_engine()

    return stop_app
