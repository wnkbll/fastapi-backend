from datetime import datetime

from sqlalchemy import MetaData, Integer, String, ForeignKey, Text, DateTime, func
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
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["TasksTable"]] = relationship(
        back_populates="user",
    )


class TasksTable(Table):
    __tablename = "Tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["UsersTable"] = relationship(
        back_populates="tasks"
    )
