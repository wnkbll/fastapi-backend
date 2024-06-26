from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn

from app.models.orm.common import Model


class UserORM(Model):
    __tablename__ = "User"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, index=True)
    name: Mapped[str] = MappedColumn(String)
    age: Mapped[int] = MappedColumn(Integer)
    passport: Mapped[str] = MappedColumn(String)
