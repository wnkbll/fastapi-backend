from typing import Optional

from sqlalchemy import select, update, Executable

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.models.schemas.users import UserInDB
from src.models.tables import UsersTable


class UsersRepository(Repository):
    async def get_user_by_username(self, *, username: str) -> UserInDB:
        query: Executable = select(UsersTable).where(UsersTable.username == username)

        async with self.session_factory() as session:
            response = await session.execute(query)

            user_row: UsersTable = response.scalars().first()
            if user_row is not None:
                return UserInDB.model_validate(user_row, from_attributes=True)

            raise EntityDoesNotExistError(f"User with username:{username} does not exist")

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        query: Executable = select(UsersTable).where(UsersTable.email == email)

        async with self.session_factory() as session:
            response = await session.execute(query)

            user_row: UsersTable = response.scalars().first()
            if user_row is not None:
                return UserInDB.model_validate(user_row, from_attributes=True)

            raise EntityDoesNotExistError(f"User with email:{email} does not exist")

    async def create_user(self, *, username: str, email: str, password: str) -> UserInDB:
        user_in_db = UserInDB(username=username, email=email)
        user_in_db.change_password(password)

        user = UsersTable(username=username, email=email, hashed_password=user_in_db.hashed_password)

        async with self.session_factory() as session:
            session.add(user)
            await session.commit()

        return user_in_db.model_validate(user, from_attributes=True)

    async def update_user(
            self,
            *,
            user: UserInDB,
            username: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            bio: Optional[str] = None,
            image: Optional[str] = None,
    ) -> UserInDB:
        user_to_change = await self.get_user_by_username(username=user.username)

        user_to_change.username = username or user_to_change.username
        user_to_change.email = email or user_to_change.email
        user_to_change.bio = bio or user_to_change.bio
        user_to_change.image = image or user_to_change.image

        if password:
            user_to_change.change_password(password)

        query: Executable = (
            update(UsersTable).
            values(
                username=user_to_change.username,
                email=user_to_change.email,
                bio=user_to_change.bio,
                image=user_to_change.image,
                hashed_password=user_to_change.hashed_password,
            ).
            filter_by(username=user.username)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return user_to_change
