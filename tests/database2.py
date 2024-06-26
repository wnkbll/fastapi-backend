from app.models.alchemy import User, UserModel


def main():
    user_orm = UserModel(id=1, name="Bob", age=18, passport="001")
    user_dto = User.model_validate(user_orm, from_attributes=True)
    print(user_dto)


if __name__ == "__main__":
    main()
