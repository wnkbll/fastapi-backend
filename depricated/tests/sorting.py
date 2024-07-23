import asyncio

from pydantic import TypeAdapter

from depricated.src.db import get_postgres_connection
from depricated.src.db import get_redis_connection
from depricated.src.db import TasksRepository
from src.models.schemas.tasks import Task


async def main():
    db_connection = get_postgres_connection()
    redis_connection = get_redis_connection()

    tasks_repo = TasksRepository(db_connection.session_factory)
    tasks = await tasks_repo.get_all()

    type_adapter = TypeAdapter(list[Task])
    encoded = type_adapter.dump_json(tasks).decode("utf-8")

    await redis_connection.set("tasks", encoded)

    value: bytes = await redis_connection.get("tasks")

    print(type_adapter.validate_json(value))


asyncio.run(main())
