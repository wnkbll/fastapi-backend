from src.db import db_postgres as postgres
from src.db import db_redis as redis


async def create_start_app_handler() -> None:
    await postgres.initialize_database()
    await redis.set_tasks()


async def create_stop_app_handler() -> None:
    await redis.flush_all()
