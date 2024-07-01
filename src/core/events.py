from typing import Callable

from src.core.settings import get_app_logger
from src.db.events import init_models, get_db_connection

logger = get_app_logger()
db_connection = get_db_connection()


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await init_models(db_connection.engine)

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        logger.info("Database engine was disposed")
        await db_connection.dispose_engine()

    return stop_app
