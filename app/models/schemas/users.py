from typing import Optional

from pydantic import EmailStr, HttpUrl

from app.models.schemas.base import AppModel, IDModelMixin
from app.services import security


class UserSchema(AppModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(IDModelMixin, UserSchema):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)


class UserInLoginSchema(AppModel):
    email: EmailStr
    password: str


class UserInCreateSchema(UserInLoginSchema):
    username: str


class UserInUpdate(AppModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(UserSchema):
    token: str


class UserInResponse(AppModel):
    user: UserWithToken
