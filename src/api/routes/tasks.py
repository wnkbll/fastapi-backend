from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body

from src.api.dependencies import TasksRepositoryDepends
from src.db.errors import EntityDoesNotExistError
from src.models.tasks import TaskInResponse, TasksInResponse, TaskInCreate, TaskInUpdate
from src.services.tasks import TasksService

router = APIRouter()


@router.get(
    "", name="tasks:get-all-tasks", response_model=TasksInResponse
)
async def get_all_tasks(
        tasks_repo: TasksRepositoryDepends,
        username: str | None = None,
) -> TasksInResponse:
    try:
        tasks = await TasksService.get_all_tasks(tasks_repo=tasks_repo, username=username)
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
    try:
        task = await TasksService.get_task_by_id(tasks_repo=tasks_repo, id_=id_)
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
        task = await TasksService.create_task(tasks_repo=tasks_repo, task_in_create=task_in_create)
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
        task = await TasksService.update_task(tasks_repo=tasks_repo, id_=id_, task_in_update=task_in_update)
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
        task = await TasksService.delete_task(tasks_repo=tasks_repo, id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id",
        ) from existence_error

    return TaskInResponse(
        task=task
    )
