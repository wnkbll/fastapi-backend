from src.db.postgres import Postgres
from src.db.redis import Redis
from src.services.tasks import TasksService


async def create_start_app_handler() -> None:
    await Postgres.initialize_database()
    await TasksService.cache_tasks()


async def create_stop_app_handler() -> None:
    await Redis.flush_all()
