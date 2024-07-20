from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body

from src.core.dependencies import TasksRepositoryDepends
from src.db.errors import EntityDoesNotExistError
from src.models.schemas.tasks import TaskInResponse, TasksInResponse, TaskInCreate, TaskInUpdate

router = APIRouter()


@router.get(
    "", name="tasks:get-all-tasks", response_model=TasksInResponse
)
async def get_all_tasks_(
        tasks_repo: TasksRepositoryDepends
) -> TasksInResponse:
    try:
        tasks = await tasks_repo.get_all()
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
    "/{username}", name="tasks:get-all-tasks-by-username", response_model=TasksInResponse
)
async def get_all_tasks_by_username(
        username: str, tasks_repo: TasksRepositoryDepends
) -> TasksInResponse:
    try:
        tasks = await tasks_repo.get_all(username=username)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        ) from existence_error

    return TasksInResponse(
        tasks=tasks,
        count=len(tasks),
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
    "/{id: int}", name="task:update-task", response_model=TaskInResponse
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
    "/{id: int}", name="task:delete-task", response_model=TaskInResponse
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
