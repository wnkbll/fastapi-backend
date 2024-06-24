from app.models.alchemy.common import Model

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn


class User(Model):
    __tablename__ = "User"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, index=True)
    name: Mapped[str] = MappedColumn(String)
    age: Mapped[int] = MappedColumn(Integer)
    passport: Mapped[str] = MappedColumn(String)
