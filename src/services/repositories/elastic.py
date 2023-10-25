import logging

from fastapi import Depends
from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from src.db.elastic import get_elastic
from services.repositories.utils.elastic_query_builder import ElasticQuery

logger = logging.getLogger(__name__)


class ElasticRepository:
    query_builder: ElasticQuery = ElasticQuery

    def __init__(self, elastic: AsyncElasticsearch = Depends(get_elastic)):
        self.elastic = elastic

    async def get(self, index: str, uuid: str) -> ObjectApiResponse | None:
        doc = await self.elastic.get(index=index, id=uuid)
        logger.info('%s was sourced from Elastic', index)
        return doc

    async def get_list(self, index: str, **kwargs) -> ObjectApiResponse:
        qb = self.query_builder(index=index, **kwargs)
        query = qb.get_query()
        return await self.elastic.search(**query)
