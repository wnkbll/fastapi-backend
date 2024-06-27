import logging

from fastapi import FastAPI

from app.api.routes import router
from app.core.environments import Environment
from app.core.settings import get_app_settings, get_app_logger
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    settings: Environment = get_app_settings()
    logger: logging.Logger = get_app_logger()

    application: FastAPI = FastAPI(**settings.fastapi_kwargs)

    application.add_event_handler(
        "startup",
        create_start_app_handler(),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(),
    )

    application.include_router(router, prefix=settings.api_prefix)

    logger.info("Application successfully initialized")

    return application


app: FastAPI = get_application()

# TODO: Rework models
# TODO: Add exception handlers
# TODO: Add middlewares (find out what is it)
# TODO: Add exception handler for repo response
