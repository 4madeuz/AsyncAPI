import hashlib
import logging
import orjson

from typing import Any, Callable, Dict, Tuple
from fastapi import Depends, Response
from src.services.person import PersonService, get_person_service

from functools import wraps
from src.models import persons


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

logger = logging.getLogger(__name__)


def key_builder(
    func: Callable[..., Any],
    *,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    cache_key = hashlib.md5(  # noqa: S324
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()
    ).hexdigest()
    return cache_key


def cache():
    def wrapper(func):

        @wraps(func)
        async def inner_wrapper(*args, service: PersonService = Depends(get_person_service), **kwargs):
            response_data = await func(*args, **kwargs, service=service,)
            cache_key = key_builder(
                func,
                args=args,
                kwargs=kwargs,
            )
            _cache = await service.redis.get(cache_key)
            if _cache:
                mapping_raw = orjson.loads(_cache)
                if 'items' in mapping_raw:
                    raw = orjson.dumps(mapping_raw['items'])
                else:
                    raw = orjson.dumps(mapping_raw)
                return (
                    Response(content=raw, media_type="application/json")
                )
            logger.info('Sourced from elastic')
            if isinstance(response_data, list):
                p_list = persons.PersonList(items=response_data)
                cached = await service.redis.set(
                    name=cache_key, value=p_list.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)
            else:
                cached = await service.redis.set(
                    name=cache_key, value=response_data.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)
            if cached:
                logger.info('Added to cache')
            return response_data

        return inner_wrapper

    return wrapper
