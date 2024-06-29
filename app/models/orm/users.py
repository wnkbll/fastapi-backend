from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn

from app.models.orm.common import Model


class UserORM(Model):
    __tablename__ = "User"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, index=True)
    username: Mapped[str] = MappedColumn(String)
    email: Mapped[str] = MappedColumn(Integer)
    bio: Mapped[str] = MappedColumn(String)
    image: Mapped[str] = MappedColumn(String)
    hashed_password: Mapped[str] = MappedColumn(String)
