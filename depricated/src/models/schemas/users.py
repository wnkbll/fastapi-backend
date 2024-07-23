from pydantic import BaseModel, EmailStr

from src.models.schemas.base import IDModelMixin
from src.services import security


class User(BaseModel):
    username: str
    email: EmailStr


class UserInDB(User, IDModelMixin):
    hashed_password: str = ""

    def verify_password(self, password: str) -> bool:
        return security.verify_password(password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.hashed_password = security.get_hashed_password(password, security.generate_salt())


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None


class UserWithToken(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithToken
