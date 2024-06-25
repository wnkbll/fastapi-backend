from dotenv import dotenv_values

env_file = "../.env"

env = dotenv_values(env_file)

print(env["DATABASE_URL"])
