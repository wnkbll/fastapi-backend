from fastapi import APIRouter

from src.api.routes import default, articles, authentication

router = APIRouter()

router.include_router(default.router, tags=["Default"], prefix="/default")
router.include_router(articles.router, tags=["Articles"], prefix="/articles")
router.include_router(authentication.router, tags=["Auth"], prefix="/auth")

__all__ = [
    "router",
]
