from fastapi import APIRouter, Depends

from src.models import films
from src.services.annotations import PageNumber, PageSize
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '',
    response_model=list[films.Genre],
    summary='Genre list',
    description='Get genres list',
)
async def genres_list(
    page_number: PageNumber.annotations() = PageNumber.default(),
    page_size: PageSize.annotations() = PageSize.default(),
    service: GenreService = Depends(get_genre_service)
) -> list[films.Genre]:
    genres = await service.get_genres(page_number, page_size)
    return genres


@router.get(
    '/{genre_id}',
    response_model=films.Genre,
    summary='Genre detail',
    description='Get detail info about genre',
)
async def genre_detail(
        genre_id: str,
        service: GenreService = Depends(get_genre_service)
) -> films.Genre:

    genre = await service.get_by_id(genre_id)
    return genre
