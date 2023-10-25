import pytest

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
async def test_all_films(make_get_request, query_data, expected_body_len):
    response = await make_get_request('/films', query_data=query_data)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == expected_body_len


@pytest.mark.asyncio
async def test_search_film_by_id(make_get_request):
    films = await make_get_request('/films', query_data={'page_size': 1})

    random_film = films['body'][0]
    response = await make_get_request(f'/films/{random_film["uuid"]}')

    assert response['status'] == HTTPStatus.OK
    assert response['body']['title'] == random_film['title']
    assert response['body']['imdb_rating'] == random_film['imdb_rating']


@pytest.mark.parametrize(
    'query_data, expected_body_len',
    [
        ({'query': 'The Star'}, 50),
        ({'query': 'My Friend'}, 0),
        ({'query': 'The Sta', 'page_number': 4, 'page_size': 30}, 10),
        ({'query': 'The Str', 'page_number': 5, 'page_size': 60}, 0),
    ]
)
@pytest.mark.asyncio
async def test_search_films_endpoint(make_get_request, query_data, expected_body_len):
    response = await make_get_request('/films/search', query_data=query_data)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == expected_body_len
