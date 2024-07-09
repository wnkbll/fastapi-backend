from pydantic import BaseModel

from src.models.schemas.base import IDModelMixin


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    author_id: int


class ArticleInDB(Article, IDModelMixin):
    pass


class ArticleInCreate(BaseModel):
    title: str
    description: str
    body: str
    username: str


class ArticleForResponse(Article):
    pass


class ArticleInResponse(BaseModel):
    article: ArticleForResponse


class ListOfArticlesInResponse(BaseModel):
    articles: list[ArticleForResponse]
    articles_count: int
