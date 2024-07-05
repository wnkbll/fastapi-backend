from fastapi import APIRouter

from src.api.routes import default, articles

router = APIRouter()

router.include_router(default.router, tags=["Default"], prefix="/default")
router.include_router(articles.router, tags=["Articles"], prefix="/articles")

__all__ = [
    "router",
]
