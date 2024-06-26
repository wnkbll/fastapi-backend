from fastapi import FastAPI

from app.api.routes import router
from app.core import get_app_settings
from app.core.environments import Environment


def get_application() -> FastAPI:
    settings: Environment = get_app_settings()

    application: FastAPI = FastAPI(**settings.fastapi_kwargs)

    application.include_router(router, prefix=settings.api_prefix)

    return application


app: FastAPI = get_application()

# TODO: Fix naming
# TODO: Fix models module(Alchemy and pydantic models in same file? Plus naming)
# TODO: Maybe some fixes in core module
# TODO: Add validation in repositories
