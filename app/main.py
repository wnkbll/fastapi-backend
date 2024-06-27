import logging

from fastapi import FastAPI

from app.api.routes import router
from app.core.environments import Environment
from app.core import get_app_settings, get_app_logger


def get_application() -> FastAPI:
    settings: Environment = get_app_settings()
    logger: logging.Logger = get_app_logger()

    application: FastAPI = FastAPI(**settings.fastapi_kwargs)

    application.include_router(router, prefix=settings.api_prefix)

    logger.info("Application successfully initialized")

    return application


app: FastAPI = get_application()

# TODO: Add initialization of models(Basemodel.metadata.create_all)
# TODO: Add logger
