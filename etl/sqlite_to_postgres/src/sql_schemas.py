from dataclasses import dataclass
from enum import Enum


@dataclass
class SQL:
    query = None
    values = None


@dataclass
class FilmWorkSQL(SQL):
    query = """INSERT INTO content.film_work (
            id, title, description, creation_date, type, rating,
            file_path, created, modified
            ) VALUES {};"""
    values = '(%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())'


@dataclass
class PersonSQL(SQL):
    query = """INSERT INTO content.person (
             id, full_name, created, modified
             ) VALUES {}"""
    values = '(%s, %s, NOW(), NOW())'


@dataclass
class GenreSQL(SQL):
    query = """INSERT INTO content.genre (
            id, name, description, created, modified
            ) VALUES {}"""
    values = '(%s, %s, %s, NOW(), NOW())'


@dataclass
class GenreFilmWorkSQL(SQL):
    query = """INSERT INTO content.genre_film_work (
            id, genre_id, film_work_id, created
            ) VALUES {}"""
    values = '(%s, %s, %s, NOW())'


@dataclass
class PersonFilmWorkSQL(SQL):
    query = """INSERT INTO content.person_film_work (
             id, person_id, film_work_id, role, created
             )  VALUES {}"""
    values = '(%s, %s, %s, %s, NOW())'


class Tables(Enum):
    FILM_WORK = 'film_work'
    PERSON = 'person'
    GENRE = 'genre'
    PERSON_FILM_WORK = 'person_film_work'
    GENRE_FILM_WORK = 'genre_film_work'
