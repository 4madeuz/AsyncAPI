import psycopg2
import pytest

from sqlite_to_postgres import config
from sqlite_to_postgres.src.extract_data import SQLiteExtractor, SQLiteManager


@pytest.fixture(scope='session')
def sessions():
    with SQLiteManager(url=config.SQLITE_DB_URL) as sqlite_conn, \
            psycopg2.connect(**config.DSL) as pg_conn:
        yield {'sqlite': sqlite_conn, 'psycopg': pg_conn}


@pytest.fixture(scope='session')
def tables():
    return (
        'content.film_work',
        'content.genre',
        'content.person',
        'content.genre_film_work',
        'content.person_film_work',
    )


@pytest.fixture(scope='session')
def truncate_table_data(sessions, tables):
    conn = sessions['psycopg']
    cursor = conn.cursor()
    for table in tables:
        query = """TRUNCATE {} CASCADE;""".format(table)
        cursor.execute(query)


@pytest.fixture(scope='session')
def sqlite_extractor(sessions):
    conn = sessions['sqlite']
    sql_extr = SQLiteExtractor(_session=conn).extract_films
    return sql_extr
