import sqlite3

import config
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from src import schemas, sql_schemas
from src.extract_data import SQLiteExtractor, SQLiteManager
from src.save_data import PostgresSaver

from etl.logs.logger import logger


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sql_extr = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)
    tables = [table.value for table in sql_schemas.Tables]

    for table in tables:
        data_from_sqlite = sql_extr.extract_data(table)

        while True:
            records = data_from_sqlite.fetchmany(config.CHUNK_SIZE)
            if len(records) == 0:
                break
            data = table, records
            dataclass_data = schemas.to_dataclass(data)
            postgres_saver.save_data(dataclass_data)


if __name__ == '__main__':
    with SQLiteManager(url=config.SQLITE_DB_URL) as sqlite_session, \
            psycopg2.connect(**config.DSL, cursor_factory=DictCursor) as pg_conn:
        try:
            load_from_sqlite(sqlite_session, pg_conn)

        except sqlite3.Error as sqlite_er:
            args = ' '.join(sqlite_er.args)
            logger.critical('While reading data from SQLite an error occurred\n'
                            'SQLite error: {}\n'
                            'SQLite error class: {}'
                            'The transaction was rolled back', args, sqlite_er.__class__
                            )

            sqlite_session.rollback()

        except (
                psycopg2.OperationalError,
                psycopg2.DataError,
                psycopg2.IntegrityError,
        ) as pg_er:
            logger.critical('An error occurred while saving data:\n'
                            '{}'
                            'The transaction was rolled back', pg_er.pgerror
                            )

    pg_conn.close()
