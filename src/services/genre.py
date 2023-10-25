import logging

from functools import lru_cache

from elasticsearch import NotFoundError
from fastapi import Depends

from src.models.films import Genre
from src.services.repositories.elastic import ElasticRepository
from src.services.repositories.base import AsyncCacheStorage
from src.services.repositories.redis import RedisRepository

logger = logging.Logger(__name__)


class GenreService:
    __elastic_index = 'genres'

    def __init__(self, redis_repo: AsyncCacheStorage, elastic_repo: ElasticRepository):
        self.redis_repo = redis_repo
        self.elastic_repo = elastic_repo

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre_from_cache = await self.redis_repo.get(index=self.__elastic_index, uuid=genre_id)
        if genre_from_cache:
            return Genre(**genre_from_cache['_source'])

        try:
            doc = await self.elastic_repo.get(index=self.__elastic_index, uuid=genre_id)
        except NotFoundError:
            return None

        await self.redis_repo.set(index=self.__elastic_index, value=doc, uuid=genre_id)
        return Genre(**doc['_source'])

    async def get_genres(
            self,
            page_number: int,
            page_size: int,
            **kwargs,
             ) -> list[Genre]:
        params = {
            'page_number': page_number,
            'page_size': page_size,
            **kwargs,
        }
        genres_from_cache = await self.redis_repo.get(index=self.__elastic_index, **params)
        if genres_from_cache:
            genres = genres_from_cache['hits']['hits']
            return [Genre(**genre['_source']) for genre in genres]

        try:
            docs = await self.elastic_repo.get_list(index=self.__elastic_index, **params)
        except NotFoundError:
            return []

        await self.redis_repo.set(index=self.__elastic_index, value=docs, **params)
        genres = docs['hits']['hits']
        return [Genre(**genre['_source']) for genre in genres]


@lru_cache()
def get_genre_service(
        redis_repo: AsyncCacheStorage = Depends(RedisRepository),
        elastic_repo: ElasticRepository = Depends(ElasticRepository),
) -> GenreService:
    return GenreService(redis_repo, elastic_repo)
