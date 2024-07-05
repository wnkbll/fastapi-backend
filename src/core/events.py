from typing import Callable

from src.db.connection import get_db_connection


def create_start_app_handler() -> Callable:
    async def start_app():
        db_connection = get_db_connection()
        await db_connection.init_db()

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        db_connection = get_db_connection()
        await db_connection.dispose_engine()

    return stop_app
