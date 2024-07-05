import asyncio

from src.core.environments import EnvironmentTypes
from src.db.connection import get_db_connection
from src.db.repositories.articles import ArticlesRepository
from src.db.repositories.users import UsersRepository


async def main() -> None:
    db_connection = get_db_connection(EnvironmentTypes.test)
    await db_connection.init_db()

    user_repo = UsersRepository(db_connection.session_factory)
    articles_repo = ArticlesRepository(db_connection.session_factory)

    await user_repo.create_user(username="Bob", email="some.address1@gmail.com", password="123456")
    await user_repo.create_user(username="Man", email="some.address2@gmail.com", password="123456")
    await user_repo.create_user(username="Alice", email="some.address3@gmail.com", password="123456")
    await user_repo.create_user(username="Tracy", email="some.address4@gmail.com", password="123456")
    await user_repo.create_user(username="Tom", email="some.address5@gmail.com", password="123456")

    user_by_username = await user_repo.get_user_by_username(username="Alice")
    user_by_email = await user_repo.get_user_by_email(email="some.address4@gmail.com")

    print(user_by_username.model_dump())
    print(user_by_email.model_dump())
    print("---------------------------------")

    await user_repo.update_user(
        user=user_by_username,
        username="Joe",
        password="654321",
        email="some.address6@gmail.com",
        bio="some text about me"
    )

    user_by_username = await user_repo.get_user_by_username(username="Joe")
    print(user_by_username.model_dump())
    print("---------------------------------")

    await articles_repo.create_article(name="Article1", text="Some text for article1", username="Man")
    await articles_repo.create_article(name="Article2", text="Some text for article2", username="Man")
    await articles_repo.create_article(name="Article3", text="Some text for article3", username="Bob")
    await articles_repo.create_article(name="Article4", text="Some text for article4", username="Bob")
    await articles_repo.create_article(name="Article5", text="Some text for article5", username="Bob")
    await articles_repo.create_article(name="Article6", text="Some text for article6", username="Tom")
    await articles_repo.create_article(name="Article7", text="Some text for article7", username="Tracy")
    await articles_repo.create_article(name="Article8", text="Some text for article8", username="Tracy")

    articles = await articles_repo.get_articles_by_author_username(username="Bob")

    for article in articles:
        print(article.model_dump())
    print("---------------------------------")


if __name__ == '__main__':
    asyncio.run(main())
