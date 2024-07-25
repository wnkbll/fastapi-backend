from datetime import datetime, timedelta, UTC

from loguru import logger
from pydantic import TypeAdapter

from src.api.dependencies import get_async_session_factory
from src.core.config import get_app_settings
from src.core.settings import Settings
from src.db.redis import Redis
from src.db.repositories.tasks import TasksRepository
from src.models.tasks import Task, TaskInCreate, TaskInUpdate


class TasksService:
    settings: Settings = get_app_settings()

    @staticmethod
    async def set_task(*, task: Task) -> None:
        type_adapter = TypeAdapter(Task)
        encoded = type_adapter.dump_json(task).decode("utf-8")
        await Redis.set(key=f"{TasksService.settings.prefixes.tasks_prefix}:{task.id}", value=encoded)

    @staticmethod
    async def delete_task_from_redis(*, id_: int) -> None:
        await Redis.delete(key=f"{TasksService.settings.prefixes.tasks_prefix}:{id_}")

    @staticmethod
    async def is_task_cached(*, id_: int) -> bool:
        return await Redis.exists(key=f"{TasksService.settings.prefixes.tasks_prefix}:{id_}")

    @staticmethod
    async def get_task_from_redis(*, id_: int) -> Task | None:
        encoded = await Redis.get(key=f"{TasksService.settings.prefixes.tasks_prefix}:{id_}")

        if encoded is None:
            return None

        type_adapter = TypeAdapter(Task)
        decoded = type_adapter.validate_json(encoded)

        logger.info(f"Tasks with id:{id_} was read from redis")

        return decoded

    @staticmethod
    async def cache_tasks() -> None:
        tasks_repo: TasksRepository = TasksRepository(get_async_session_factory())
        tasks = await tasks_repo.get_all(sort_by_deadline=True)

        await Redis.flush_all()

        for task in tasks:
            await TasksService.set_task(task=task)

        logger.info("Tasks info was successfully updated")

    @staticmethod
    async def get_all_tasks(*, tasks_repo: TasksRepository, username: str = None) -> list[Task]:
        tasks = (
            await tasks_repo.get_all(username=username)
            if username else
            await tasks_repo.get_all()
        )

        return tasks

    @staticmethod
    async def get_task_by_id(*, tasks_repo: TasksRepository, id_: int) -> Task:
        task = await TasksService.get_task_from_redis(id_=id_)

        if task is not None:
            return task

        return await tasks_repo.get(id_=id_)

    @staticmethod
    async def create_task(*, tasks_repo: TasksRepository, task_in_create: TaskInCreate) -> Task:
        task = await tasks_repo.create(task_in_create=task_in_create)

        if all((task.deadline - datetime.now(UTC) <= timedelta(days=3), task.deadline > datetime.now(UTC))):
            await TasksService.set_task(task=task)

        return task

    @staticmethod
    async def update_task(*, tasks_repo: TasksRepository, id_: int, task_in_update: TaskInUpdate) -> Task:
        task = await tasks_repo.update(id_=id_, task_in_update=task_in_update)

        if all((task.deadline - datetime.now(UTC) <= timedelta(days=3), task.deadline > datetime.now(UTC))):
            await TasksService.set_task(task=task)

        return task

    @staticmethod
    async def delete_task(*, tasks_repo: TasksRepository, id_: int, ) -> Task:
        task = await tasks_repo.delete(id_=id_)

        if await TasksService.is_task_cached(id_=id_):
            await TasksService.delete_task_from_redis(id_=id_)

        return task
