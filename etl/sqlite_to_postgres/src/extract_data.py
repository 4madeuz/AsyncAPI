import sqlite3

from dotenv import load_dotenv

load_dotenv()


class SQLiteManager:

    def __init__(self, connect=sqlite3.connect, url=None):
        self.connect = connect
        self.url = url

    def __enter__(self):
        self.session = self.connect(self.url)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.close()
        else:
            self.session.rollback()
            self.session.close()


class SQLiteExtractor:

    def __init__(self, _session: sqlite3.Connection, row_factory=sqlite3.Row):
        self.session = _session
        self.session.row_factory = row_factory

    def extract_data(self, table: str) -> sqlite3.Cursor:
        cursor = self.session.cursor()
        query = """SELECT * FROM {table}""".format(table=table)
        cursor.execute(query)
        return cursor
