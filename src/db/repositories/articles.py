from sqlalchemy import select, Executable
from sqlalchemy.orm import selectinload

from src.db.errors import EntityDoesNotExistError
from src.db.repositories.repository import Repository
from src.models.schemas.articles import ArticleInDB
from src.models.tables import UsersTable, ArticlesTable
from src.services import articles


class ArticlesRepository(Repository):
    async def get_articles_by_author_username(self, *, username: str) -> list[ArticleInDB]:
        query: Executable = (
            select(UsersTable).
            where(UsersTable.username == username).
            options(selectinload(UsersTable.articles))
        )

        async with self.session_factory() as session:
            response = await session.execute(query)
            user_with_articles = response.scalars().first()

            if user_with_articles is None:
                raise EntityDoesNotExistError

            articles = []
            for article in user_with_articles.articles:
                article_in_db = ArticleInDB.model_validate(article, from_attributes=True)
                articles.append(article_in_db)

            return articles

    async def create_article(self, *, title: str, description: str, body: str, username: str) -> ArticleInDB:
        query: Executable = select(UsersTable).where(UsersTable.username == username)

        async with self.session_factory() as session:
            response = await session.execute(query)
            user_row = response.scalars().first()
            article = ArticlesTable(
                slug=articles.get_slug_for_article(title), title=title, description=description, body=body, user=user_row,
            )
            session.add(article)
            await session.commit()
            article_in_db = ArticleInDB.model_validate(article, from_attributes=True)

        return article_in_db

    async def update_article(self, *, username: str) -> ArticleInDB:
        pass

    async def delete_article(self) -> None:
        pass

    async def get_article_by_slug(self) -> ArticleInDB:
        pass
