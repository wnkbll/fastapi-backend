import asyncio

from src.core.environments import EnvironmentTypes
from src.db.connection import get_db_connection
from src.db.repositories.articles import ArticlesRepository
from src.db.repositories.users import UsersRepository
from src.models.schemas.users import UserInCreate, UserInUpdate
from src.models.schemas.articles import ArticleInCreate


async def main() -> None:
    db_connection = get_db_connection(EnvironmentTypes.test)
    await db_connection.init_db()

    users_repo = UsersRepository(db_connection.session_factory)
    articles_repo = ArticlesRepository(db_connection.session_factory)

    user1 = UserInCreate(username="Bob", email="some.address1@gmail.com", password="123456")
    user2 = UserInCreate(username="Man", email="some.address2@gmail.com", password="123456")
    user3 = UserInCreate(username="Alice", email="some.address3@gmail.com", password="123456")
    user4 = UserInCreate(username="Tracy", email="some.address4@gmail.com", password="123456")
    user5 = UserInCreate(username="Tom", email="some.address5@gmail.com", password="123456")

    await users_repo.create_user(user_in_create=user1)
    await users_repo.create_user(user_in_create=user2)
    await users_repo.create_user(user_in_create=user3)
    await users_repo.create_user(user_in_create=user4)
    await users_repo.create_user(user_in_create=user5)

    user_by_username = await users_repo.get_user_by_username(username="Alice")
    user_by_email = await users_repo.get_user_by_email(email="some.address4@gmail.com")

    print(user_by_username.verify_password("123456"))
    print(user_by_username.verify_password("654321"))
    print(user_by_username.model_dump())
    print(user_by_email.model_dump())
    print("---------------------------------")

    user_in_update = UserInUpdate(
        username="Joe",
        password="654321",
        email="some.address6@gmail.com",
        bio="some text about me"
    )

    await users_repo.update_user(
        username=user_by_username.username,
        user_in_update=user_in_update,
    )

    user_by_username = await users_repo.get_user_by_username(username="Joe")
    print(user_by_username.verify_password("123456"))
    print(user_by_username.verify_password("654321"))
    print(user_by_username.model_dump())
    print("---------------------------------")

    article1 = ArticleInCreate(
        title="Article1", description="Some desc for article1", body="Some text for article1", username="Man",
    )
    article2 = ArticleInCreate(
        title="Article2", description="Some desc for article2", body="Some text for article2", username="Man",
    )
    article3 = ArticleInCreate(
        title="Article3", description="Some desc for article3", body="Some text for article3", username="Bob",
    )
    article4 = ArticleInCreate(
        title="Article4", description="Some desc for article4", body="Some text for article4", username="Bob",
    )
    article5 = ArticleInCreate(
        title="Article5", description="Some desc for article5", body="Some text for article5", username="Bob",
    )
    article6 = ArticleInCreate(
        title="Article6", description="Some desc for article6", body="Some text for article6", username="Tom",
    )
    article7 = ArticleInCreate(
        title="Article7", description="Some desc for article7", body="Some text for article7", username="Tracy",
    )
    article8 = ArticleInCreate(
        title="Article8", description="Some desc for article8", body="Some text for article8", username="Tracy",
    )

    await articles_repo.create_article(article_in_create=article1)
    await articles_repo.create_article(article_in_create=article2)
    await articles_repo.create_article(article_in_create=article3)
    await articles_repo.create_article(article_in_create=article4)
    await articles_repo.create_article(article_in_create=article5)
    await articles_repo.create_article(article_in_create=article6)
    await articles_repo.create_article(article_in_create=article7)
    await articles_repo.create_article(article_in_create=article8)

    articles = await articles_repo.get_articles_by_author_username(username="Bob")

    for article in articles:
        print(article.model_dump())
    print("---------------------------------")


if __name__ == '__main__':
    asyncio.run(main())
