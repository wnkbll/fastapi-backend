from sqlalchemy import select, update, Executable

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.models.schemas.users import UserInDB, UserInCreate, UserInUpdate
from src.models.tables import UsersTable


class UsersRepository(Repository):
    async def get_user_by_email(self, *, email: str) -> UserInDB:
        query: Executable = select(UsersTable).where(UsersTable.email == email)

        async with self.session_factory() as session:
            response = await session.execute(query)

            user_row: UsersTable = response.scalars().first()
            if user_row is not None:
                return UserInDB.model_validate(user_row, from_attributes=True)

            raise EntityDoesNotExistError(f"User with email:{email} does not exist")

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        query: Executable = select(UsersTable).where(UsersTable.username == username)

        async with self.session_factory() as session:
            response = await session.execute(query)

            user_row: UsersTable = response.scalars().first()
            if user_row is not None:
                return UserInDB.model_validate(user_row, from_attributes=True)

            raise EntityDoesNotExistError(f"User with username:{username} does not exist")

    async def create_user(self, *, user_in_create: UserInCreate) -> UserInDB:
        user_in_db = UserInDB(username=user_in_create.username, email=user_in_create.email)
        user_in_db.change_password(user_in_create.password)

        user_row = UsersTable(
            username=user_in_create.username, email=user_in_create.email, hashed_password=user_in_db.hashed_password
        )

        async with self.session_factory() as session:
            session.add(user_row)
            await session.commit()

        return user_in_db.model_validate(user_row, from_attributes=True)

    async def update_user(self, *, username: str, user_in_update: UserInUpdate) -> UserInDB:
        user_to_change = await self.get_user_by_username(username=username)

        user_to_change.username = user_in_update.username or user_to_change.username
        user_to_change.email = user_in_update.email or user_to_change.email
        user_to_change.bio = user_in_update.bio or user_to_change.bio
        user_to_change.image = user_in_update.image or user_to_change.image

        if user_in_update.password:
            user_to_change.change_password(user_in_update.password)

        query: Executable = (
            update(UsersTable).
            values(
                username=user_to_change.username,
                email=user_to_change.email,
                bio=user_to_change.bio,
                image=user_to_change.image,
                hashed_password=user_to_change.hashed_password,
            ).
            filter_by(username=username)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return user_to_change
