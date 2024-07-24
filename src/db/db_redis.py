from loguru import logger
from pydantic import TypeAdapter
from redis import asyncio as aioredis

from src.api.dependencies import get_async_session_factory
from src.core.config import get_app_settings
from src.db.repositories.tasks import TasksRepository
from src.models.tasks import Task


async def flush_all() -> None:
    settings = get_app_settings()
    redis = aioredis.from_url(settings.redis_dsn)

    async with redis.client() as connection:
        await connection.flushall()

    logger.info("Redis database was flushed")


async def set_tasks() -> None:
    settings = get_app_settings()
    tasks_repo: TasksRepository = TasksRepository(get_async_session_factory())
    type_adapter = TypeAdapter(Task)
    redis = aioredis.from_url(settings.redis_dsn)

    tasks = await tasks_repo.get_all(sort_by_deadline=True)

    async with redis.client() as connection:
        await connection.flushall()
        for task in tasks:
            encoded = type_adapter.dump_json(task).decode("utf-8")
            await connection.set(task.id, encoded)

    logger.info("Tasks info was successfully updated")


async def get_task(id_: int) -> Task | None:
    settings = get_app_settings()
    type_adapter = TypeAdapter(Task)
    redis = aioredis.from_url(settings.redis_dsn)

    async with redis.client() as connection:
        encoded = await connection.get(id_)

        if encoded is None:
            return None

        decoded = type_adapter.validate_json(encoded)

    logger.info(f"Tasks with id: {id_} was read from redis")
    return decoded
