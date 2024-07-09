import bcrypt


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def get_hashed_password(password: str, salt: str) -> str:
    return bcrypt.hashpw(password.encode(), salt.encode()).decode()
