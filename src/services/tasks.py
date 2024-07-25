from loguru import logger
from pydantic import TypeAdapter

from src.api.dependencies import get_async_session_factory
from src.db.redis import Redis
from src.db.repositories.tasks import TasksRepository
from src.models.tasks import Task


class TasksService:
    @staticmethod
    async def get_task_from_redis(*, id_: int) -> Task | None:
        encoded = await Redis.get(key=id_)

        if encoded is None:
            return None

        type_adapter = TypeAdapter(Task)
        decoded = type_adapter.validate_json(encoded)

        logger.info(f"Tasks with id: {id_} was read from redis")

        return decoded

    @staticmethod
    async def cache_tasks() -> None:
        type_adapter = TypeAdapter(Task)
        tasks_repo: TasksRepository = TasksRepository(get_async_session_factory())
        tasks = await tasks_repo.get_all(sort_by_deadline=True)

        await Redis.flush_all()

        for task in tasks:
            encoded = type_adapter.dump_json(task).decode("utf-8")
            await Redis.set(key=task.id, value=encoded)

        logger.info("Tasks info was successfully updated")

    @staticmethod
    async def get_all_tasks(*, tasks_repo: TasksRepository, username: str = None) -> list[Task]:
        tasks = await tasks_repo.get_all(username=username) if username else await tasks_repo.get_all()

        return tasks

    @staticmethod
    async def get_task_by_id(*, tasks_repo: TasksRepository, id_: int) -> Task:
        task = await TasksService.get_task_from_redis(id_=id_)

        if task is not None:
            return task

        return await tasks_repo.get(id_=id_)
