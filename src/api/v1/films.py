from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.models import films as film_
from src.services.annotations import PageNumber, PageSize
from src.services.film import FilmService, get_film_service, MessagesToUser

router = APIRouter()


@router.get(
    '/search',
    response_model=list[film_.FilmShort],
    summary='Search films',
    description='Get films list filtered by query',
)
async def search_films(
        query: str | None,
        sort: str | None = None,
        page_number: PageNumber.annotations() = PageNumber.default(),
        page_size: PageSize.annotations() = PageSize.default(),
        service: FilmService = Depends(get_film_service),
) -> list[film_.FilmShort]:

    films_ = await service.get_films_list(page_number, page_size, query=query, sort=sort)
    return films_


@router.get(
    '/{film_id}',
    response_model=film_.FilmFull,
    summary='Films detail',
    description='Get film detail by film id',
)
async def film_detail(film_id: str, service: FilmService = Depends(get_film_service)) -> film_.FilmFull:
    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MessagesToUser.NOT_FOUND)

    return film


@router.get(
    '',
    response_model=list[film_.FilmShort],
    summary='Films list',
    description='Get film list',
)
async def films_list(
        sort: str | None = None,
        genre: str | None = None,
        page_number: PageNumber.annotations() = PageNumber.default(),
        page_size: PageSize.annotations() = PageSize.default(),
        service: FilmService = Depends(get_film_service),
) -> list[film_.FilmShort]:

    films = await service.get_films_list(page_number, page_size, genre=genre, sort=sort)
    return films
