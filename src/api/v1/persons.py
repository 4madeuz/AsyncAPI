from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.models import persons
from src.services.annotations import PageSize, PageNumber
from src.services.person import PersonService, get_person_service, MessagesToUser

router = APIRouter()


@router.get(
    '',
    response_model=list[persons.Person],
    summary='Get persons list',
    description='Get persons list sorted by query param',
)
async def persons_list(
        query: str | None = None,
        page_number: PageNumber.annotations() = PageNumber.default(),
        page_size: PageSize.annotations() = PageSize.default(),
        service: PersonService = Depends(get_person_service)
     ) -> list[persons.Person]:
    _persons = await service.get_persons(page_number, page_size, query=query)
    return _persons


@router.get(
    '/{person_id}',
    response_model=persons.PersonDetail,
    summary='Person detail',
    description='Get detail info about user by user id',
)
async def person_detail(
        person_id: str,
        service: PersonService = Depends(get_person_service)
) -> persons.PersonDetail:

    person = await service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MessagesToUser.NOT_FOUND)
    return person
