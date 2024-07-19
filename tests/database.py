import asyncio
from datetime import datetime

from src.core.environments import EnvironmentTypes
from src.db.connection import get_db_connection
from src.db.repositories.tasks import TasksRepository
from src.db.repositories.users import UsersRepository
from src.models.schemas.tasks import TaskInCreate, TaskInUpdate
from src.models.schemas.users import UserInCreate, UserInUpdate


async def main() -> None:
    db_connection = get_db_connection(EnvironmentTypes.test)
    await db_connection.init_db()

    users_repo = UsersRepository(db_connection.session_factory)
    task_repo = TasksRepository(db_connection.session_factory)

    user1 = UserInCreate(username="Bob", email="some.address1@gmail.com", password="123456")
    user2 = UserInCreate(username="Man", email="some.address2@gmail.com", password="123456")
    user3 = UserInCreate(username="Alice", email="some.address3@gmail.com", password="123456")
    user4 = UserInCreate(username="Tracy", email="some.address4@gmail.com", password="123456")
    user5 = UserInCreate(username="Tom", email="some.address5@gmail.com", password="123456")

    await users_repo.create(user_in_create=user1)
    await users_repo.create(user_in_create=user2)
    await users_repo.create(user_in_create=user3)
    await users_repo.create(user_in_create=user4)
    await users_repo.create(user_in_create=user5)

    user_by_username = await users_repo.get(username="Alice")
    user_by_email = await users_repo.get(email="some.address4@gmail.com")

    print(user_by_username.verify_password("123456"))
    print(user_by_username.verify_password("654321"))
    print(user_by_username.model_dump())
    print(user_by_email.model_dump())
    print("---------------------------------")

    user_in_update = UserInUpdate(
        username="Joe",
        password="654321",
        email="some.address6@gmail.com",
        bio="some text about me"
    )

    await users_repo.update(
        username=user_by_username.username,
        user_in_update=user_in_update,
    )

    user_by_username = await users_repo.get(username="Joe")
    print(user_by_username.verify_password("123456"))
    print(user_by_username.verify_password("654321"))
    print(user_by_username.model_dump())
    print("---------------------------------")

    users = await users_repo.get_all()
    for user in users:
        print(user.model_dump())
    print("---------------------------------")

    task1 = TaskInCreate(
        title="Task1", description="Some desc for task1",
        body="Some text for task1", deadline=datetime(2024, 8, 1, 0, 0, 0), username="Man",
    )
    task2 = TaskInCreate(
        title="Task2", description="Some desc for task2",
        body="Some text for task2", deadline=datetime(2024, 8, 2, 0, 0, 0), username="Man",
    )
    task3 = TaskInCreate(
        title="Task3", description="Some desc for task3",
        body="Some text for task3", deadline=datetime(2024, 8, 3, 0, 0, 0), username="Bob",
    )
    task4 = TaskInCreate(
        title="Task4", description="Some desc for task4",
        body="Some text for task4", deadline=datetime(2024, 8, 4, 0, 0, 0), username="Bob",
    )
    task5 = TaskInCreate(
        title="Task5", description="Some desc for task5",
        body="Some text for task5", deadline=datetime(2024, 8, 5, 0, 0, 0), username="Bob",
    )
    task6 = TaskInCreate(
        title="Task6", description="Some desc for task6",
        body="Some text for task6", deadline=datetime(2024, 8, 6, 0, 0, 0), username="Tom",
    )
    task7 = TaskInCreate(
        title="Task7", description="Some desc for task7",
        body="Some text for task7", deadline=datetime(2024, 8, 7, 0, 0, 0), username="Tracy",
    )
    task8 = TaskInCreate(
        title="Task8", description="Some desc for task8",
        body="Some text for task8", deadline=datetime(2024, 8, 8, 0, 0, 0), username="Tracy",
    )

    await task_repo.create(task_in_create=task1)
    await task_repo.create(task_in_create=task2)
    await task_repo.create(task_in_create=task3)
    await task_repo.create(task_in_create=task4)
    await task_repo.create(task_in_create=task5)
    await task_repo.create(task_in_create=task6)
    await task_repo.create(task_in_create=task7)
    await task_repo.create(task_in_create=task8)

    tasks = await task_repo.get_all(username="Bob")
    for task in tasks:
        print(task.model_dump())
    print("---------------------------------")

    task_in_update = TaskInUpdate(
        title="UpdatedTitleForTask7",
        deadline=datetime(2024, 8, 15, 0, 0, 0)
    )
    task_to_update = await task_repo.get(id_=7)
    await task_repo.update(id_=task_to_update.id_, task_in_update=task_in_update)

    tasks = await task_repo.get_all()
    for task in tasks:
        print(task.model_dump())
    print("---------------------------------")


if __name__ == '__main__':
    asyncio.run(main())
