from typing import Callable

from fastapi import APIRouter, Depends, Body, HTTPException, status

from src.db.connection import get_db_connection, DatabaseConnection
from src.db.errors import EntityDoesNotExistError
from src.db.repositories.articles import ArticlesRepository
from src.db.repositories.repository import Repository
from src.models.schemas.articles import (
    ArticleInCreate,
    ArticleInResponse,
    ArticleForResponse,
    ListOfArticlesInResponse,
)

router = APIRouter()


# TODO Move this function to dependencies module
def get_repository(repository: type[Repository]) -> Callable[[DatabaseConnection], Repository]:
    def __get_repo(db_connection: DatabaseConnection = Depends(get_db_connection)) -> Repository:
        return repository(db_connection.session_factory)

    return __get_repo


@router.get("/{username}", name="articles:get-all-articles-from-user", response_model=ListOfArticlesInResponse)
async def get_all_articles(
        username: str,
        articles_repo: ArticlesRepository = Depends(get_repository(ArticlesRepository)),
) -> ListOfArticlesInResponse:
    articles = await articles_repo.get_articles_by_author_username(username=username)

    articles_for_response = [
        ArticleForResponse(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            author_id=article.author_id,
        ) for article in articles
    ]

    return ListOfArticlesInResponse(
        articles=articles_for_response,
        articles_count=len(articles_for_response),
    )


@router.post("", name="articles:create-article", response_model=ArticleInResponse)
async def create_article(
        article_in_create: ArticleInCreate = Body(alias="article"),
        articles_repo: ArticlesRepository = Depends(get_repository(ArticlesRepository)),
) -> ArticleInResponse:
    try:
        article_in_db = await articles_repo.create_article(article_in_create=article_in_create)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {article_in_create.username} does not exists"
        )

    article_for_response = ArticleForResponse(
        slug=article_in_db.slug,
        title=article_in_db.title,
        description=article_in_db.description,
        body=article_in_db.body,
        author_id=article_in_db.author_id,
    )

    return ArticleInResponse(
        article=article_for_response,
    )
