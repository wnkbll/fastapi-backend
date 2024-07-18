from sqlalchemy import select, Executable
from sqlalchemy.orm import selectinload

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.models.schemas.tasks import Task, TaskInCreate, TaskInUpdate
from src.models.tables import TasksTable, UsersTable


class TasksRepository(Repository):
    async def create(self, *, task_in_create: TaskInCreate) -> Task:
        query: Executable = select(UsersTable).filter_by(username=task_in_create.username)

        task = TasksTable(
            title=task_in_create.title, description=task_in_create.description,
            body=task_in_create.body, deadline=task_in_create.deadline,
        )

        async with self.session_factory() as session:
            response = await session.execute(query)

            user_row = response.scalars().first()
            if user_row is None:
                raise EntityDoesNotExistError(f"User with username:{task_in_create.username} does not exist")

            task.user = user_row

            session.add(task)
            await session.commit()

        return Task.model_validate(task, from_attributes=True)

    async def get(self, *, id_: int) -> Task:
        query: Executable = select(TasksTable).filter_by(id=id_)

        async with self.session_factory() as session:
            response = await session.execute(query)

            task_row = response.scalars().first()
            if task_row is None:
                raise EntityDoesNotExistError(f"Task with id:{id_} does not exist")

            return Task.model_validate(task_row, from_attributes=True)

    async def get_all(self, username: str = None) -> list[Task]:
        query: Executable = (
            select(UsersTable).filter_by(username=username).options(selectinload(UsersTable.tasks))
            if username else
            select(TasksTable)
        )

        async with self.session_factory() as session:
            response = await session.execute(query)

            if username is None:
                user_with_tasks = response.scalars().first()

                if user_with_tasks is None:
                    raise EntityDoesNotExistError(f"User with username:{username} does not exist")

                return [
                    Task.model_validate(task, from_attributes=True) for task in user_with_tasks.tasks
                ]

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
