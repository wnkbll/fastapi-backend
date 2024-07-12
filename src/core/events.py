from src.db.connection import get_db_connection


async def create_start_app_handler() -> None:
    db_connection = get_db_connection()
    await db_connection.init_db()


async def create_stop_app_handler() -> None:
    db_connection = get_db_connection()
    await db_connection.dispose_engine()
