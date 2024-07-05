from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.tables.table import Table


class UsersTable(Table):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    articles: Mapped[list["ArticlesTable"]] = relationship(
        back_populates="user",
    )


class ArticlesTable(Table):
    __tablename__ = "Articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["UsersTable"] = relationship(
        back_populates="articles",
    )


__all__ = [
    "Table",
    "UsersTable",
    "ArticlesTable",
]
