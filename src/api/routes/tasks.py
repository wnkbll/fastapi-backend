from fastapi import APIRouter, HTTPException, status

from src.db.errors import EntityDoesNotExistError
from src.models.schemas.tasks import TasksInResponse
from src.core.dependencies import TasksRepositoryDepends

router = APIRouter()


@router.get(
    "/", name="tasks:get-all-tasks", response_model=TasksInResponse
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
