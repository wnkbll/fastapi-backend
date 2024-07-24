import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.routes import router
from src.core.config import get_app_settings
from src.core.events import create_start_app_handler, create_stop_app_handler
from src.core.paths import LOGGING_DIR
from src.core.settings import Settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_start_app_handler()
    yield
    await create_stop_app_handler()


def get_application() -> FastAPI:
    settings: Settings = get_app_settings()

    logger.configure(
        handlers=[
            dict(
                sink=LOGGING_DIR.joinpath(settings.logging.file),
                level="WARNING",
                rotation=settings.logging.rotation,
                compression=settings.logging.compression,
                serialize=True,
            ),
            dict(
                sink=sys.stderr,
                level="TRACE",
            ),
        ],
    )

    application: FastAPI = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)

    application.include_router(router, prefix=settings.api_prefix)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.middleware.allow_origins,
        allow_credentials=settings.middleware.allow_credentials,
        allow_methods=settings.middleware.allow_methods,
        allow_headers=settings.middleware.allow_headers,
    )

    return application


app: FastAPI = get_application()


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def http_exception_handler(
        _: Request, exc: RequestValidationError | ValidationError
) -> JSONResponse:
    return JSONResponse({"errors": [exc.errors()]}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
