from src.db.errors import EntityDoesNotExistError
from src.db.repositories.users import UsersRepository


async def is_username_taken(users_repo: UsersRepository, username: str) -> bool:
    try:
        await users_repo.get_user_by_username(username=username)
    except EntityDoesNotExistError:
        return False

    return True


async def is_email_taken(users_repo: UsersRepository, email: str) -> bool:
    try:
        await users_repo.get_user_by_email(email=email)
    except EntityDoesNotExistError:
        return False

    return True
