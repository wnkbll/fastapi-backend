from typing import Callable

from fastapi import APIRouter, Depends

from src.db.connection import get_db_connection, DatabaseConnection
from src.db.repositories.articles import ArticlesRepository
from src.db.repositories.repository import Repository
from src.models.schemas.articles import ArticleInDB

router = APIRouter()


# TODO Move this function to dependencies module
def get_repository(repository: type[Repository]) -> Callable[[DatabaseConnection], Repository]:
    def __get_repo(db_connection: DatabaseConnection = Depends(get_db_connection)) -> Repository:
        return repository(db_connection.session_factory)

    return __get_repo


@router.get("/{username}", name="articles:get-all-articles", response_model=list[ArticleInDB])
async def get_all_articles(
        username: str,
        articles_repo: ArticlesRepository = Depends(get_repository(ArticlesRepository))
):
    articles = await articles_repo.get_articles_by_author_username(username=username)
    return articles
