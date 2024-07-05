from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from src.models.schemas.base import IDModelMixin


class User(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(User, IDModelMixin):
    hashed_password: str = ""

    def is_correct_password(self, password: str) -> bool:
        return self.hashed_password == password  # TODO: Add security module

    def change_password(self, password: str) -> None:
        self.hashed_password = password  # TODO: Add security module
