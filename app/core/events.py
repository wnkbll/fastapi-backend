from typing import Callable

from app.db.events import init_models
from app.db.connection import get_db_connection
from app.core.settings import get_app_logger

logger = get_app_logger()
db_connection = get_db_connection()


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await init_models(db_connection.get_engine())

    return start_app


def create_stop_app_handler() -> Callable:
    def stop_app() -> None:
        db_connection.dispose_engine()

    return stop_app
