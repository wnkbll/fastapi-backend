from typing import Optional

from pydantic import EmailStr, HttpUrl, Field

from app.models.schemas.base import AppModel, IDModelMixin
from app.services import security


class User(AppModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(IDModelMixin, User):
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.hashed_password = security.get_password_hash(password)


class UserInLogin(AppModel):
    email: EmailStr = Field()
    password: str = Field()


class UserInCreate(UserInLogin):
    username: str = Field()


class UserInUpdate(AppModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(User):
    token: str


class UserInResponse(AppModel):
    user: UserWithToken
