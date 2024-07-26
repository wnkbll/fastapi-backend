# FastAPI backend application

## Getting Started

### Dependencies
* Docker Engine - https://docs.docker.com/engine/install/
* Docker Compose - https://docs.docker.com/compose/install/

### Installing
Before starting, make sure you have the latest versions of Docker installed.

Run the following commands to pull this repo from GitHub and get to src folder:
```
git clone https://github.com/wnkbll/fastapi-backend.git
cd fastapi-backend
```
Create the ```.env.prod``` file or rename the ```.env.example``` file and put there this values:
```
DB_HOST=db                    # name of postgres container defined in docker-compose.yml file
DB_PORT=1221                  # port of postgres container defined in docker-compose.yml file
DB_NAME=postgres              # database name defined in POSTGRES_DB variable
DB_USER=postgres              # superuser's name defined in POSTGRES_USER variable
DB_PASS=postgres              # superuser's password defined in POSTGRES_PASSWORD variable

POSTGRES_DB=postgres          # postgres variable with defenition of database name
POSTGRES_USER=postgres        # postgres variable with defenition of superuser's name
POSTGRES_PASSWORD=postgres    # postgres variable with defenition of superuser's password

REDIS_HOST=redis              # name of redis container defined in docker-compose.yml file
REDIS_PORT=5370               # port of redis container defined in docker-compose.yml file

SECRET_KEY=secret             # secret str using for creating jwt
```

### Run With Docker
You must have ```docker``` and ```docker-compose``` tools installed to work with material in this section.
Head to the root folder of the project.
To run the program, we spin up the containers with
```
docker compose build
docker compose up
```

### Project Structure
```bash
├───resources                   # related with project docs, diagrams, etc.
├───scripts                     # bash scripts for docker
├───src
│   ├───api
│   │   ├───dependencies.py     # FastAPI dependency injection 
│   │   └───routes              # FastAPI endpoints
│   ├───core                    # settings, paths
│   ├───db
│   │   ├───tables.py           # SQLAlchemy models
│   │   └───repositories        # CRUD related stuff
│   ├───models                  # Pydantic models
│   └───services                # Services for jwt generation, hashing passwords, etc.
│   └───migrations              
│       └───versions            # Alembic autogenerated migrations
└───tests
```
