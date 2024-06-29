import requests


def main() -> None:
    response = requests.post(
        'http://127.0.0.1:8000/api/users/login',
        json={
            "user_login": {
                "email": "some.address1@gmail.com",
                "password": "123456"
            }
        })
    print(response.json())


if __name__ == '__main__':
    main()
