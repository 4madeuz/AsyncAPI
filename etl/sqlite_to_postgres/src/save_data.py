from dataclasses import asdict

from . import schemas, sql_schemas


class PostgresSaver:

    def __init__(self, connect):
        self.cursor = connect.cursor()

    def save_data(self, db_data: tuple[str, list[schemas.Table]]) -> None:
        table, records = db_data
        sql = self.get_sql(table)
        fields = [tuple(asdict(rec).values()) for rec in records]

        args = ','.join(
            self.cursor.mogrify(sql.values, item).decode() for item in fields
        )
        self.cursor.execute(sql.query.format(args))

    @staticmethod
    def get_sql(table: str) -> sql_schemas.SQL:
        sql_query_mapper = {
            'genre': sql_schemas.GenreSQL(),
            'genre_film_work': sql_schemas.GenreFilmWorkSQL(),
            'person_film_work': sql_schemas.PersonFilmWorkSQL(),
            'person': sql_schemas.PersonSQL(),
            'film_work': sql_schemas.FilmWorkSQL(),
        }
        return sql_query_mapper.get(table)
