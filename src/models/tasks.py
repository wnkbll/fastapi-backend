from datetime import datetime

from pydantic import BaseModel

from src.models.base import IDModelMixin, TimestampsModelMixin


class Task(IDModelMixin, TimestampsModelMixin):
    title: str
    description: str
    body: str
    deadline: datetime
    is_complete: bool
    user_id: int


class TaskInCreate(BaseModel):
    title: str | None
    description: str | None
    body: str
    deadline: datetime
    username: str


class TaskInUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None
    deadline: datetime | None = None
    is_complete: bool | None = None


class TaskInResponse(BaseModel):
    task: Task


class TasksInResponse(BaseModel):
    tasks: list[Task]
    count: int
