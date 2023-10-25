import pytest
import orjson

from http import HTTPStatus


@pytest.mark.parametrize(
    'query_data, expected_body_len',
    [
        ({}, 50),
        ({'page_number': 5, 'page_size': 5}, 5),
        ({'page_size': 80}, 80),
        ({'page_size': 30, 'page_number': 2}, 30),
        ({'page_number': 5, 'page_size': 70}, 0),
    ]
)
@pytest.mark.asyncio
async def test_all_genres(make_get_request, query_data, expected_body_len):
    response = await make_get_request('/genres', query_data=query_data)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == expected_body_len


@pytest.mark.parametrize(
    'query_data, cache_key',
    [
        ({'page_number': 1, 'page_size': 50}, '9335044906b6e1b51466368da2c95170'),
        ({'query': 'Actio', 'page_number': 4, 'page_size': 30}, 'f5542365cb694de48d377fbb368169ff'),
    ]
)
@pytest.mark.asyncio
async def test_redis_genres(make_get_request, redis_client, query_data, cache_key):
    response = await make_get_request('/genres', query_data=query_data)

    _cache = await redis_client.get(name=cache_key)
    mapping_raw = orjson.loads(_cache)

    assert response['body'] == [obj['_source'] for obj in mapping_raw['hits']['hits']]


@pytest.mark.asyncio
async def test_genres_id(make_get_request):
    genres = await make_get_request('/genres')
    random_genre = genres['body'][0]

    response = await make_get_request(f'/genres/{random_genre["uuid"]}')

    assert response['status'] == HTTPStatus.OK
    assert response['body']['name'] == random_genre['name']
