import uuid
from dataclasses import dataclass
from enum import Enum


@dataclass
class ElasticFilmRecord:
    uuid: uuid.uuid4
    imdb_rating: float
    genre: list[dict]
    title: str
    description: str
    director: str
    actors_names: list[str]
    writers_names: list[str]
    actors: list[dict]
    writers: list[dict]
    directors: list[dict]


@dataclass
class ElasticGenreRecord:
    uuid: uuid.uuid4
    name: str


@dataclass
class ElasticPersonRecord:
    uuid: uuid.uuid4
    full_name: str
    actors: list[dict]
    writers: list[dict]
    directors: list[dict]


class RoleType(Enum):
    ACTOR = 'actor'
    DIRECTOR = 'director'
    WRITER = 'writer'
