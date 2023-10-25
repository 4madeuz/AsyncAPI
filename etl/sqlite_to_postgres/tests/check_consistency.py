from sqlite_to_postgres.load_data import load_from_sqlite


def test_data_consistency(
        sessions, sqlite_extractor, truncate_table_data, tables
):
    sqlite_conn = sessions['sqlite']
    pg_conn = sessions['psycopg']
    load_from_sqlite(connection=sqlite_conn, pg_conn=pg_conn)
    cursor = pg_conn.cursor()

    for table in tables:
        sqlite_table_name = table.split('.')[1]
        sqlite_data = sqlite_extractor(sqlite_table_name).fetchall()
        query = """SELECT count(*) FROM {}""".format(table)
        cursor.execute(query)
        assert cursor.fetchone()[0] == len(sqlite_data)


def test_equals_records_in_film_work_tables(sessions, sqlite_extractor):
    pg_conn = sessions['psycopg']
    cursor = pg_conn.cursor()
    film_works_from_sqlite = sqlite_extractor('film_work').fetchall()

    for film in film_works_from_sqlite:
        query = """SELECT title, rating
        FROM content.film_work
        WHERE id='{}'""".format(film['id'])
        cursor.execute(query)
        title, rating = cursor.fetchone()
        assert title == film['title']
        assert rating == film['rating']


def test_equals_records_in_genre_tables(sessions, sqlite_extractor):
    pg_conn = sessions['psycopg']
    cursor = pg_conn.cursor()
    genres_from_sqlite = sqlite_extractor('genre').fetchall()

    for genre in genres_from_sqlite:
        query = """SELECT name
        FROM content.genre
        WHERE id='{}'""".format(genre['id'])
        cursor.execute(query)
        genre_name = cursor.fetchone()[0]
        assert genre_name == genre['name']


def test_equals_records_in_person_tables(sessions, sqlite_extractor):
    pg_conn = sessions['psycopg']
    cursor = pg_conn.cursor()
    persons_from_sqlite = sqlite_extractor('person').fetchall()

    for person in persons_from_sqlite:
        query = """SELECT full_name
        FROM content.person
        WHERE id='{}'""".format(person['id'])
        cursor.execute(query)
        person_full_name = cursor.fetchone()[0]
        assert person_full_name == person['full_name']


def test_equals_records_in_person_film_works_tables(
        sessions, sqlite_extractor
):
    pg_conn = sessions['psycopg']
    cursor = pg_conn.cursor()
    person_film_works_from_sqlite = sqlite_extractor('person_film_work').fetchall()

    for pfw in person_film_works_from_sqlite:
        query = """SELECT person_id, film_work_id, role
        FROM content.person_film_work
        WHERE id='{}'""".format(pfw['id'])
        cursor.execute(query)
        person_id, film_work_id, role = cursor.fetchone()
        assert person_id == pfw['person_id']
        assert film_work_id == pfw['film_work_id']
        assert role == pfw['role']


def test_equals_records_in_genre_film_work_tables(
        sessions, sqlite_extractor
):
    pg_conn = sessions['psycopg']
    cursor = pg_conn.cursor()
    genre_film_works_from_sqlite = sqlite_extractor('genre_film_work').fetchall()

    for gfw in genre_film_works_from_sqlite:
        query = """SELECT genre_id, film_work_id
                FROM content.genre_film_work
                WHERE id='{}'""".format(gfw['id'])
        cursor.execute(query)
        genre_id, film_work_id = cursor.fetchone()
        assert genre_id == gfw['genre_id']
        assert film_work_id == gfw['film_work_id']
