from src.models import base
from elastic_transport import ObjectApiResponse


class Person(base.Model):
    full_name: str


class Actor(Person):
    pass


class Director(Person):
    pass


class Writer(Person):
    pass


class FilmTitle(base.Model):
    title: str


class PersonDetail(Person):
    actors: list[FilmTitle]
    writers: list[FilmTitle]
    directors: list[FilmTitle]

    @classmethod
    def to_films_models(cls, data):
        if isinstance(data, ObjectApiResponse):
            source = data['_source']
            cls._to_films(source)
            return

        persons = [person['_source'] for person in data]
        for person in persons:
            cls._to_films(person)

    @classmethod
    def _to_films(cls, obj):
        obj['actors'] = [FilmTitle(**film) for film in obj['actors']]
        obj['writers'] = [FilmTitle(**film) for film in obj['writers']]
        obj['directors'] = [FilmTitle(**film) for film in obj['directors']]


class PersonList(base.ListModel):
    items: list
