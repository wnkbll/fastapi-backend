from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body

from src.api.dependencies import TasksRepositoryDepends
from src.db import db_redis as redis
from src.db.errors import EntityDoesNotExistError
from src.models.tasks import TaskInResponse, TasksInResponse, TaskInCreate, TaskInUpdate

router = APIRouter()


@router.get(
    "", name="tasks:get-all-tasks", response_model=TasksInResponse
)
async def get_all_tasks(
        tasks_repo: TasksRepositoryDepends,
        username: str | None = None,
) -> TasksInResponse:
    try:
        tasks = await tasks_repo.get_all(username=username) if username else await tasks_repo.get_all()
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        ) from existence_error

    return TasksInResponse(
        tasks=tasks,
        count=len(tasks),
    )


@router.get(
    "/{id_}", name="tasks:get-task-by-id", response_model=TaskInResponse
)
async def get_task_by_id(
        id_: int, tasks_repo: TasksRepositoryDepends
) -> TaskInResponse:
    task = await redis.get_task(id_)

    if task is not None:
        return TaskInResponse(
            task=task
        )

    try:
        task = await tasks_repo.get(id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no tasks with this id:{id_}",
        ) from existence_error

    return TaskInResponse(
        task=task
    )


@router.post(
    "", name="tasks:create-task", response_model=TaskInResponse
)
async def create_task(
        tasks_repo: TasksRepositoryDepends,
        task_in_create: Annotated[TaskInCreate, Body(alias="task-in-create")],
) -> TaskInResponse:
    try:
        task = await tasks_repo.create(task_in_create=task_in_create)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        ) from existence_error

    return TaskInResponse(
        task=task
    )


@router.put(
    "/{id_}", name="task:update-task", response_model=TaskInResponse
)
async def update_task(
        id_: int,
        tasks_repo: TasksRepositoryDepends,
        task_in_update: Annotated[TaskInUpdate, Body(alias="task-in-update")],
) -> TaskInResponse:
    try:
        task = await tasks_repo.update(id_=id_, task_in_update=task_in_update)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id",
        ) from existence_error

    return TaskInResponse(
        task=task
    )


@router.delete(
    "/{id_}", name="task:delete-task", response_model=TaskInResponse
)
async def delete_task(
        id_: int,
        tasks_repo: TasksRepositoryDepends,
) -> TaskInResponse:
    try:
        task = await tasks_repo.delete(id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id",
        ) from existence_error

    return TaskInResponse(
        task=task
    )
