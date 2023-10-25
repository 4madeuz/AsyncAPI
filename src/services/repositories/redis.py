import logging

import typing
from redis import Redis
from fastapi import Depends
from elastic_transport import ObjectApiResponse

from src.core import config
from src.db.redis import get_redis
from src.services.repositories.base import AsyncCacheStorage
from src.services.repositories.utils.redis_formatter import RedisFormatter
from src.services.repositories.utils.key_builder import key_builder

logger = logging.getLogger(__name__)

MoviesEntity: typing.TypeAlias = dict


class RedisRepository(AsyncCacheStorage):
    __decode_format = 'utf-8'

    def __init__(self, redis: Redis = Depends(get_redis), formatter: RedisFormatter = Depends(RedisFormatter)):
        self.redis = redis
        self.formatter = formatter

    async def get(self, index: str, **kwargs) -> MoviesEntity | None:
        key = key_builder(index=index, params=kwargs)
        entities = await self.redis.get(name=key)
        if not entities:
            return

        logger.info('Value for %s get from cache', key)
        return self.formatter.to_dict(entities)

    async def set(self, index: str, value: ObjectApiResponse, **kwargs) -> None:
        value = self.formatter.to_bytes(value.body)
        key = key_builder(index=index, params=kwargs)
        await self.redis.set(name=key, value=value, ex=config.settings.redis_keys_expiration)
