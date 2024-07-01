import asyncio

from src.models.tables import Table
from src.db.events import get_db_connection
from src.db.repositories.users import UsersRepository


async def main() -> None:
    db_connection = get_db_connection()
    user_repo = UsersRepository(db_connection.session_factory)

    async with db_connection.engine.begin() as conn:
        await conn.run_sync(Table.metadata.drop_all)
        await conn.run_sync(Table.metadata.create_all)

    await user_repo.create_user(username="Bob", email="some.address1@gmail.com", password="123456")
    await user_repo.create_user(username="Man", email="some.address2@gmail.com", password="123456")
    await user_repo.create_user(username="Alice", email="some.address3@gmail.com", password="123456")
    await user_repo.create_user(username="Tracy", email="some.address4@gmail.com", password="123456")
    await user_repo.create_user(username="Tom", email="some.address5@gmail.com", password="123456")

    user_by_username = await user_repo.get_user_by_username(username="Alice")
    user_by_email = await user_repo.get_user_by_email(email="some.address4@gmail.com")

    print(user_by_username.model_dump())
    print(user_by_email.model_dump())
    print("---------------------------------")

    await user_repo.update_user(
        user=user_by_username,
        username="Joe",
        password="654321",
        email="some.address6@gmail.com",
        bio="some text about me"
    )

    user_by_username = await user_repo.get_user_by_username(username="Joe")
    print(user_by_username.model_dump())


if __name__ == '__main__':
    asyncio.run(main())
