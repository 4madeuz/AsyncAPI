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
async def test_all_persons(make_get_request, query_data, expected_body_len):
    response = await make_get_request('/persons', query_data=query_data)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == expected_body_len


@pytest.mark.parametrize(
    'query_data, expected_body_len',
    [
        ({'query': 'Mark Hamill'}, 50),
        ({'query': 'Luke Skywalker'}, 0),
        ({'query': 'Mark', 'page_number': 4, 'page_size': 30}, 10),
        ({'query': 'Hamill', 'page_number': 5, 'page_size': 60}, 0),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(make_get_request, query_data, expected_body_len):
    response = await make_get_request('/persons', query_data=query_data)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == expected_body_len


@pytest.mark.asyncio
async def test_persons_id(make_get_request):
    persons = await make_get_request('/persons', query_data={'page_size': 1})
    random_person = persons['body'][0]

    response = await make_get_request(f'/persons/{random_person["uuid"]}')

    assert response['status'] == HTTPStatus.OK
    assert response['body']['full_name'] == random_person['full_name']
    assert response['body']['actors'][0]['title'] == 'Star Slammer'
    assert response['body']['writers'][0]['title'] == 'Star Slammer'
    assert response['body']['directors'][0]['title'] == 'Star Slammer'
