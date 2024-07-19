from datetime import datetime

from pydantic import BaseModel

from src.models.schemas.base import IDModelMixin


class Task(BaseModel, IDModelMixin):
    title: str
    description: str
    body: str
    deadline: datetime
    created_at: datetime
    updated_at: datetime
    user_id: int


class TaskInCreate(BaseModel):
    title: str | None
    description: str | None
    body: str
    deadline: datetime
    username: str


class TaskInUpdate(BaseModel):
    title: str | None
    description: str | None
    body: str | None
    deadline: datetime | None


class TaskInResponse(BaseModel):
    task: Task


class TasksInResponse(BaseModel):
    tasks: list[Task]
    count: int
