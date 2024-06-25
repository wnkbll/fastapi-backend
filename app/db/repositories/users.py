from sqlalchemy import Executable, select, update, delete

from app.models.alchemy import UserModel, User
from app.db.repositories.repository import Repository


class UsersRepository(Repository[UserModel]):
    async def get(self, _id: int) -> User:
        async with self.session() as conn:
            query: Executable = select(UserModel).where(UserModel.id == _id)
            response = await conn.execute(query)
            return User.model_validate(response.scalars().first())

    async def get_all(self) -> list[User]:
        async with self.session() as conn:
            query: Executable = select(UserModel)
            response = await conn.execute(query)
            users = response.scalars().all()
            return [User.model_validate(user) for user in users]

    async def add(self, entity: UserModel) -> None:
        async with self.session() as conn:
            conn.add(entity)
            await conn.commit()

    async def update(self, _id: int, entity: UserModel) -> None:
        async with self.session() as conn:
            mapped_entity = {"name": entity.name, "age": entity.age, "passport": entity.passport}
            query: Executable = update(UserModel).where(UserModel.id == _id).values(mapped_entity)
            await conn.execute(query)
            await conn.commit()

    async def delete(self, _id: int) -> None:
        async with self.session() as conn:
            query: Executable = delete(UserModel).where(UserModel.id == _id)
            await conn.execute(query)
            await conn.commit()
