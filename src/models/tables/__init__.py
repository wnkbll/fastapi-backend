from sqlalchemy import MetaData, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Table(DeclarativeBase):
    convention = {
        "all_column_names": lambda constraint, table: "_".join([
            column.name for column in constraint.columns.values()
        ]),
        "ix": "ix__%(table_name)s__%(all_column_names)s",
        "uq": "uq__%(table_name)s__%(all_column_names)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s",
    }

    metadata = MetaData()
    metadata.naming_convention = convention


class UsersTable(Table):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)

    articles: Mapped[list["ArticlesTable"]] = relationship(
        back_populates="user",
    )


class ArticlesTable(Table):
    __tablename__ = "Articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["UsersTable"] = relationship(
        back_populates="articles",
    )


__all__ = [
    "Table",
    "UsersTable",
    "ArticlesTable",
]
