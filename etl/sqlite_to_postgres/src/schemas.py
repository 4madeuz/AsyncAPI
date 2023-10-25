import datetime
import sqlite3
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias


class FilmType(str, Enum):
    MOVIE: str = 'movie'
    TV_SHOW: str = 'tv_show'


@dataclass
class IDField:
    id: uuid.uuid4


@dataclass
class Genre(IDField):
    name: str
    description: str | None


@dataclass
class Filmwork(IDField):
    title: str
    description: str | None
    creation_date: datetime.date
    type: FilmType
    rating: float
    file_path: str | None


@dataclass
class Person(IDField):
    full_name: str


@dataclass
class GenreFilmwork(IDField):
    genre_id: uuid.uuid4
    film_work_id: uuid.uuid4


@dataclass
class PersonFilmwork(IDField):
    person_id: uuid.uuid4
    film_work_id: uuid.uuid4
    role: str


Table: TypeAlias = Genre | Person | Filmwork | PersonFilmwork | GenreFilmwork


def to_dataclass(db_data: [tuple[str, list[sqlite3.Row]]]) -> tuple[str, list[Table]]:
    mapper = {
        'genre': Genre,
        'genre_film_work': GenreFilmwork,
        'person': Person,
        'person_film_work': PersonFilmwork,
        'film_work': Filmwork
    }
    table, records = db_data
    _dataclass = mapper[table]
    records = [_dataclass(
        **_removed_fields_from_sqlite_row(v, _dataclass)
    ) for v in records]
    return table, records


def _removed_fields_from_sqlite_row(sqlite_row: sqlite3.Row, _dataclass) -> dict:
    data = {**sqlite_row}
    for key in data.copy():
        if key not in _dataclass.__dataclass_fields__:
            data.pop(key)
    return data
