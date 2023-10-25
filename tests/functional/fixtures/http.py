import pytest
import aiohttp

from tests.functional.settings import test_settings


@pytest.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(aiohttp_session):
    async def inner(url_path: str, query_data: dict | None = None) -> dict[str, int | str]:
        url = _get_url(url_path, query_data)

        async with aiohttp_session.get(url) as response:
            status = response.status
            body = await response.json(content_type='application/json')

        return {'status': status, 'body': body}
    return inner


def _get_url(url_path: str, queries: dict) -> str:
    url_base = test_settings.service_url + '/api/v1' + url_path
    if not queries:
        return url_base

    url_base += '?'
    queries_list = [f'{query}={value}' for query, value in queries.items()]
    url_base += '&'.join(queries_list)
    return url_base
