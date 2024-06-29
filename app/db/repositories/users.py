from typing import Optional

from sqlalchemy import Executable, select, update

from app.db.errors import EntityDoesNotExistError
from app.db.repositories.repository import Repository
from app.models.schemas.users import UserSchema, UserInDB
from app.models.tables import UsersTable


class UsersRepository(Repository):
    async def get_user_by_email(self, *, email: str) -> UserInDB:
        async with self.session_factory() as session:
            query: Executable = select(UsersTable).where(UsersTable.email == email)
            execution = await session.execute(query)

            user_row = execution.scalars().first()
            if user_row is not None:
                return UserInDB(**user_row)

            raise EntityDoesNotExistError(f"User with email:{email} does not exist")

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        async with self.session_factory() as session:
            query: Executable = select(UsersTable).where(UsersTable.username == username)
            execution = await session.execute(query)

            user_row = execution.scalars().first()
            if user_row is not None:
                return UserInDB(**user_row)

            raise EntityDoesNotExistError(f"User with username:{username} does not exist")

    async def create_user(
            self,
            *,
            username: str,
            email: str,
            password: str,
    ) -> UserInDB:
        pass

    async def update_user(
            self,
            *,
            user: UserSchema,
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

        async with self.session_factory() as session:
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

            await session.execute(query)
            await session.commit()

        return user_to_change
