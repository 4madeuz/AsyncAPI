from elastic_transport import ObjectApiResponse

from src.models import base
from src.models import persons


class Genre(base.Model):
    name: str


class FilmShort(base.Model):
    title: str
    imdb_rating: float


class FilmFull(FilmShort):
    description: str | None
    genre:  list[Genre]
    actors: list[persons.Actor]
    writers: list[persons.Writer]
    directors: list[persons.Director]

    @classmethod
    def to_persons_models(cls, data):
        if isinstance(data, (ObjectApiResponse, dict)):
            source = data['_source']
            cls._to_person(source)
            return

        films = [film['_source'] for film in data]
        for film in films:
            cls._to_person(film)

    @classmethod
    def _to_person(cls, obj):
        obj['actors'] = [persons.Actor(**actor) for actor in obj['actors']]
        obj['writers'] = [persons.Writer(**writer) for writer in obj['writers']]
        obj['directors'] = [persons.Director(**director) for director in obj['directors']]
        obj['genre'] = [Genre(**genre) for genre in obj['genre']]
