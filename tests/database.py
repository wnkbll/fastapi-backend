import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models.alchemy import Model, UserModel
from app.db.repositories import UsersRepository

DATABASE_DIALECT = "postgresql"
DATABASE_DRIVER = "asyncpg"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "admin"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"

DATABASE_URL = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)


async def main():
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    await init_models(engine)

    bob = UserModel(name="Bob", age=42, passport="001")
    sam = UserModel(name="Sam", age=25, passport="002")

    users_repository = UsersRepository(session)

    await users_repository.add(bob)
    await users_repository.add(sam)

    users = await users_repository.get_all()
    for user in users:
        print(f"id: {user.id}; name: {user.name}; age: {user.age}; passport: {user.passport}")
    print("---------------------------")

    await users_repository.update(2, UserModel(name="Alice", age=18, passport="003"))

    users = await users_repository.get_all()
    for user in users:
        print(f"id: {user.id}; name: {user.name}; age: {user.age}; passport: {user.passport}")
    print("---------------------------")

    await users_repository.delete(1)

    users = await users_repository.get_all()
    for user in users:
        print(f"id: {user.id}; name: {user.name}; age: {user.age}; passport: {user.passport}")


if __name__ == "__main__":
    asyncio.run(main())
