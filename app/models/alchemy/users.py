from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn
from pydantic import BaseModel

from app.models.alchemy.common import Model


class UserModel(Model):
    __tablename__ = "UserModel"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, index=True)
    name: Mapped[str] = MappedColumn(String)
    age: Mapped[int] = MappedColumn(Integer)
    passport: Mapped[str] = MappedColumn(String)


class User(BaseModel):
    id: int
    name: str
    age: int
    passport: str
