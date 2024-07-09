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
