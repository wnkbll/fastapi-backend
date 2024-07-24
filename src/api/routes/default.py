from fastapi import APIRouter
from loguru import logger

from src.core.config import get_app_settings

router = APIRouter()


@router.get("/", name="default:root")
async def root():
    return {"message": "OK"}


@router.get("/settings", name="default:settings")
async def get_app_info():
    settings = get_app_settings()
    info = {
        "api_prefix": settings.api_prefix,
        "postgres_dsn": settings.postgres_dsn,
        "redis_dsn": settings.redis_dsn,
        "fastapi_kwargs": settings.fastapi_kwargs,
    }

    return info


@router.get("/logger", name="default:logger")
async def logger_test():
    logger.trace("This is logger.trace call")
    logger.debug("This is logger.debug call")
    logger.info("This is logger.info call")
    logger.success("This is logger.success call")
    logger.warning("This is logger.warning call")
    logger.error("This is logger.error call")
    logger.critical("This is logger.critical call")

    return {"message": "OK"}
