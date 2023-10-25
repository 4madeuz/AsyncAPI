import pytest
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from tests.functional.settings import test_settings


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    yield client
    await client.close()
