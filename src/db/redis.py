from loguru import logger
from redis import asyncio as aioredis

from src.core.config import get_app_settings

KeyType = bytes | str | memoryview
ValueType = bytes | str | memoryview | int | float


class Redis:
    @staticmethod
    async def set(*, key: KeyType, value: ValueType) -> None:
        settings = get_app_settings()
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.set(key, value)

        logger.info(f"Key {key} was set")

    @staticmethod
    async def get(*, key: KeyType) -> ValueType:
        settings = get_app_settings()
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            encoded = await connection.get(key)

        logger.info(f"Key {key} was read")

        return encoded

    @staticmethod
    async def delete(*, key: KeyType) -> None:
        settings = get_app_settings()
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.delete(key)

        logger.info(f"Key {key} was deleted")

    @staticmethod
    async def exists(*, key: KeyType) -> bool:
        settings = get_app_settings()
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            return bool(await connection.exists(key))

    @staticmethod
    async def flush_all() -> None:
        settings = get_app_settings()
        redis = aioredis.from_url(settings.redis_dsn)

        async with redis.client() as connection:
            await connection.flushall()

        logger.info("Redis database was flushed")
