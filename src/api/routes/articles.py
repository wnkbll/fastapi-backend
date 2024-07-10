from fastapi import APIRouter, Body, HTTPException, status

from src.api.dependencies import ArticlesRepositoryDepends
from src.db.errors import EntityDoesNotExistError
from src.models.schemas.articles import (
    ArticleInCreate,
    ArticleInResponse,
    ArticleForResponse,
    ListOfArticlesInResponse,
)

router = APIRouter()


@router.get("", name="articles:get-all-articles", response_model=ListOfArticlesInResponse)
async def get_all_articles(
        articles_repo: ArticlesRepositoryDepends,
) -> ListOfArticlesInResponse:
    try:
        articles = await articles_repo.get_all_articles()
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List of articles is empty"
        )

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


@router.get("/{username}", name="articles:get-all-articles-from-user", response_model=ListOfArticlesInResponse)
async def get_all_articles_from_user(
        username: str,
        articles_repo: ArticlesRepositoryDepends,
) -> ListOfArticlesInResponse:
    try:
        articles = await articles_repo.get_articles_by_author_username(username=username)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} does not exists"
        )

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
        articles_repo: ArticlesRepositoryDepends,
        article_in_create: ArticleInCreate = Body(alias="article"),
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
