import logging
from functools import lru_cache
from dataclasses import dataclass

from fastapi import Depends
from elasticsearch import NotFoundError

from src.models.persons import Person, PersonDetail
from src.services.repositories.elastic import ElasticRepository
from src.services.repositories.base import AsyncCacheStorage
from src.services.repositories.redis import RedisRepository

logger = logging.Logger(__name__)


@dataclass
class MessagesToUser:
    NOT_FOUND = 'Person not found'


class PersonService:
    __elastic_index = 'persons'

    def __init__(self, redis_repo: AsyncCacheStorage, elastic_repo: ElasticRepository):
        self.redis_repo = redis_repo
        self.elastic_repo = elastic_repo

    async def get_by_id(self, person_id: str) -> PersonDetail | None:
        person_from_cache = await self.redis_repo.get(index=self.__elastic_index, uuid=person_id)
        if person_from_cache is not None:
            return PersonDetail(**person_from_cache['_source'])

        try:
            doc = await self.elastic_repo.get(index=self.__elastic_index, uuid=person_id)
        except NotFoundError:
            return

        await self.redis_repo.set(index=self.__elastic_index, value=doc, uuid=person_id)
        return PersonDetail(**doc['_source'])

    async def get_persons(
            self,
            page_number: int,
            page_size: int,
            **kwargs,
         ) -> list[Person]:

        params = {
            'page_number': page_number,
            'page_size': page_size,
            **kwargs,
        }
        persons_from_cache = await self.redis_repo.get(index=self.__elastic_index, **params)
        if persons_from_cache:
            persons = persons_from_cache['hits']['hits']
            return [Person(**person['_source']) for person in persons]

        try:
            docs = await self.elastic_repo.get_list(index=self.__elastic_index, **params)
        except NotFoundError:
            return []

        await self.redis_repo.set(index=self.__elastic_index, value=docs, **params)
        persons = docs['hits']['hits']
        return [Person(**person['_source']) for person in persons]


@lru_cache()
def get_person_service(
        redis_repo: AsyncCacheStorage = Depends(RedisRepository),
        elastic_repo: ElasticRepository = Depends(ElasticRepository),
) -> PersonService:
    return PersonService(redis_repo, elastic_repo)
