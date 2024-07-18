from sqlalchemy import select, update, delete, Executable

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.models.schemas.tasks import Task, TaskInCreate, TaskInUpdate
from src.models.tables import TasksTable


class TasksRepository(Repository):
    async def create(self, *, task_in_create: TaskInCreate) -> Task:
        pass

    async def get(self, *, id_: int) -> Task:
        pass

    async def get_all(self) -> list[Task]:
        query: Executable = select(TasksTable)

        async with self.session_factory() as session:
            response = await session.execute(query)
            tasks_ = response.scalars().all()

            if tasks_ is None:
                raise EntityDoesNotExistError("List of tasks is empty")

            return [
                Task.model_validate(task, from_attributes=True) for task in tasks_
            ]

    async def update(self, *, id_: int, task_in_update: TaskInUpdate) -> Task:
        pass

    async def delete(self, *, id_: int) -> Task:
        pass
