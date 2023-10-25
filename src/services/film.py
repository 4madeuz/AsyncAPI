import logging
from functools import lru_cache
from dataclasses import dataclass

from fastapi import Depends
from elasticsearch import NotFoundError

from src.models.films import FilmFull, FilmShort
from src.services.repositories.elastic import ElasticRepository
from src.services.repositories.base import AsyncCacheStorage
from src.services.repositories.redis import RedisRepository


logger = logging.getLogger(__name__)


@dataclass
class MessagesToUser:
    NOT_FOUND = 'Film not found'


class FilmService:
    __elastic_index = 'movies'

    def __init__(self, redis_repo: AsyncCacheStorage, elastic_repo: ElasticRepository):
        self.redis_repo = redis_repo
        self.elastic_repo = elastic_repo

    async def get_by_id(self, film_id: str) -> FilmFull | None:
        film_from_cache = await self.redis_repo.get(index=self.__elastic_index, uuid=film_id)
        if film_from_cache is not None:
            FilmFull.to_persons_models(film_from_cache)
            return FilmFull(**film_from_cache['_source'])

        try:
            doc = await self.elastic_repo.get(index=self.__elastic_index, uuid=film_id)
        except NotFoundError:
            return None

        await self.redis_repo.set(index=self.__elastic_index, value=doc, uuid=film_id)
        FilmFull.to_persons_models(doc)
        return FilmFull(**doc['_source'])

    async def get_films_list(self, page_number: int, page_size: int, **kwargs) -> list[FilmShort]:
        params = {
            'page_number': page_number,
            'page_size': page_size,
            **kwargs,
        }

        films_from_cache = await self.redis_repo.get(
            index=self.__elastic_index,
            **params
        )
        if films_from_cache:
            films = films_from_cache['hits']['hits']
            return [FilmShort(**film['_source']) for film in films]

        try:
            docs = await self.elastic_repo.get_list(
                index=self.__elastic_index, page_number=page_number, page_size=page_size, **kwargs
            )
        except NotFoundError:
            return []

        await self.redis_repo.set(index=self.__elastic_index, value=docs, **params)
        films = docs['hits']['hits']
        return [FilmShort(**film['_source']) for film in films]


@lru_cache()
def get_film_service(
        redis_repo: AsyncCacheStorage = Depends(RedisRepository),
        elastic_repo: ElasticRepository = Depends(ElasticRepository)
) -> FilmService:

    return FilmService(redis_repo, elastic_repo)
