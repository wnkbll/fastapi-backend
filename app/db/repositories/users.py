from sqlalchemy import Executable, select, update, delete

from app.models.orm.users import UserORM
from app.models.schemas.users import UserSchema
from app.db.repositories.repository import Repository


class UsersRepository(Repository[UserORM]):
    async def get(self, _id: int) -> UserSchema:
        async with self.session() as conn:
            query: Executable = select(UserORM).where(UserORM.id == _id)
            response = await conn.execute(query)
            return UserSchema.model_validate(response.scalars().first(), from_attributes=True)

    async def get_all(self) -> list[UserSchema]:
        async with self.session() as conn:
            query: Executable = select(UserORM)
            response = await conn.execute(query)
            users = response.scalars().all()
            return [UserSchema.model_validate(user, from_attributes=True) for user in users]

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
