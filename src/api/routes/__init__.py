from fastapi import APIRouter

from src.api.routes import default, tasks, auth

router = APIRouter()

router.include_router(default.router, tags=["Default"], prefix="/default")
router.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")
router.include_router(auth.router, tags=["Auth"], prefix="/auth")

__all__ = [
    "router",
]
