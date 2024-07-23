from src.db.db_postgres import initialize_database


async def create_start_app_handler() -> None:
    await initialize_database()


async def create_stop_app_handler() -> None:
    pass
