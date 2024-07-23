from functools import lru_cache

from redis import asyncio as aioredis

from depricated.src.core import get_app_settings
from depricated.src.core import Environment, EnvironmentTypes

KeyType = bytes | str | memoryview
ValueType = bytes | memoryview | str | int | float


class RedisConnection:
    def __init__(self, settings: Environment) -> None:
        self._url = settings.redis.url
        self.redis = aioredis.from_url(self.url)

    @property
    def url(self) -> str:
        return self._url

    async def set(self, key: KeyType, value: ValueType) -> None:
        async with self.redis.client() as connection:
            await connection.set(key, value)

    async def get(self, key: KeyType) -> ValueType:
        async with self.redis.client() as connection:
            return await connection.get(key)


@lru_cache
def get_redis_connection(env_type: EnvironmentTypes = EnvironmentTypes.dev):
    settings = get_app_settings(env_type)
    redis_connection = RedisConnection(settings)
    return redis_connection
