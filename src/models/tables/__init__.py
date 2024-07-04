from datetime import datetime, UTC
from typing import Annotated

from sqlalchemy import Integer, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.tables.table import Table

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[
    datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(UTC),
    )
]


class UsersTable(Table):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    articles: Mapped[list["ArticlesTable"]] = relationship(
        back_populates="author",
    )


class ArticlesTable(Table):
    __tablename__ = "Articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    author: Mapped["UsersTable"] = relationship(
        back_populates="articles",
    )


__all__ = [
    "Table",
    "UsersTable",
    "ArticlesTable",
]
