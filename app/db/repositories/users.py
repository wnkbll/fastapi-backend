from sqlalchemy import Executable, select, update, delete

from app.models.alchemy import User
from app.db.repositories.repository import Repository


class UsersRepository(Repository[User]):
    async def get(self, _id: int) -> User | None:
        async with self.session() as conn:
            query: Executable = select(User).where(User.id == _id)
            user = await conn.execute(query)
            return user.scalars().first()

    async def get_all(self) -> list[User]:
        async with self.session() as conn:
            query: Executable = select(User)
            users = await conn.execute(query)
            return [user for user in users.scalars().all()]

    async def add(self, entity: User) -> None:
        async with self.session() as conn:
            conn.add(entity)
            await conn.commit()

    async def update(self, _id: int, entity: User) -> None:
        async with self.session() as conn:
            mapped_entity = {"name": entity.name, "age": entity.age, "passport": entity.passport}
            query: Executable = update(User).where(User.id == _id).values(mapped_entity)
            await conn.execute(query)
            await conn.commit()

    async def delete(self, _id: int) -> None:
        async with self.session() as conn:
            query: Executable = delete(User).where(User.id == _id)
            await conn.execute(query)
            await conn.commit()
