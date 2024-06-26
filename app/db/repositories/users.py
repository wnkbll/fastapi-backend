from sqlalchemy import Executable, select, update, delete

from app.db.repositories import Repository
from app.models import UserORM, UserDTO


class UsersRepository(Repository[UserORM]):
    async def get(self, _id: int) -> UserDTO:
        async with self.session() as conn:
            query: Executable = select(UserORM).where(UserORM.id == _id)
            response = await conn.execute(query)
            return UserDTO.model_validate(response.scalars().first(), from_attributes=True)

    async def get_all(self) -> list[UserDTO]:
        async with self.session() as conn:
            query: Executable = select(UserORM)
            response = await conn.execute(query)
            users = response.scalars().all()
            return [UserDTO.model_validate(user, from_attributes=True) for user in users]

    async def add(self, entity: UserORM) -> None:
        async with self.session() as conn:
            conn.add(entity)
            await conn.commit()

    async def update(self, _id: int, entity: UserORM) -> None:
        async with self.session() as conn:
            mapped_entity = {"name": entity.name, "age": entity.age, "passport": entity.passport}
            query: Executable = update(UserORM).where(UserORM.id == _id).values(mapped_entity)
            await conn.execute(query)
            await conn.commit()

    async def delete(self, _id: int) -> None:
        async with self.session() as conn:
            query: Executable = delete(UserORM).where(UserORM.id == _id)
            await conn.execute(query)
            await conn.commit()
