from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from src.models.schemas.base import IDModelMixin
from src.services import security


class User(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(User, IDModelMixin):
    hashed_password: str = ""

    def verify_password(self, password: str) -> bool:
        return security.verify_password(password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.hashed_password = security.get_hashed_password(password, security.generate_salt())
