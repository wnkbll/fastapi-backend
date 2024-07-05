from pydantic import BaseModel

from src.models.schemas.base import IDModelMixin


class Article(BaseModel):
    name: str
    text: str
    author_id: int


class ArticleInDB(Article, IDModelMixin):
    pass
