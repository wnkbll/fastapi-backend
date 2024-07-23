from datetime import datetime, timedelta, UTC

from sqlalchemy import select, update, delete, Executable
from sqlalchemy.orm import selectinload

from depricated.src.db.errors import EntityDoesNotExistError
from depricated.src.db.repositories.repository import Repository
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

    async def get_all(self, *, username: str | None = None, sort_by_deadline: bool = False) -> list[Task]:
        username_is_none = username is None

        query: Executable = (
            select(UsersTable).filter_by(username=username).options(selectinload(UsersTable.tasks))
            if not username_is_none else
            select(TasksTable).where(TasksTable.deadline - datetime.now(UTC) <= timedelta(days=3))
            if sort_by_deadline else
            select(TasksTable)
        )

        async with self.session_factory() as session:
            response = await session.execute(query)

            if not username_is_none:
                user_with_tasks = response.scalars().first()

                if user_with_tasks is None:
                    raise EntityDoesNotExistError(f"User with username:{username} does not exist")

                return [
                    Task.model_validate(task, from_attributes=True) for task in user_with_tasks.tasks
                ]

            tasks = response.scalars().all()

            if tasks is None:
                raise EntityDoesNotExistError("List of tasks is empty")

            return [
                Task.model_validate(task, from_attributes=True) for task in tasks
            ]

    async def update(self, *, id_: int, task_in_update: TaskInUpdate) -> Task:
        task_to_change = await self.get(id_=id_)

        task_to_change.title = task_in_update.title or task_to_change.title
        task_to_change.description = task_in_update.description or task_to_change.description
        task_to_change.body = task_in_update.body or task_to_change.body
        task_to_change.deadline = task_in_update.deadline or task_to_change.deadline
        task_to_change.is_complete = task_in_update.is_complete or task_to_change.is_complete

        query: Executable = (
            update(TasksTable).
            values(
                title=task_to_change.title,
                description=task_to_change.description,
                body=task_to_change.body,
                deadline=task_to_change.deadline,
                is_complete=task_to_change.is_complete,
            ).
            filter_by(id=id_)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return task_to_change

    async def delete(self, *, id_: int) -> Task:
        task_in_db = await self.get(id_=id_)

        query: Executable = delete(TasksTable).filter_by(id=id_)

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return task_in_db
