import os

from dotenv import load_dotenv

load_dotenv()


DSL = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

SQLITE_DB_URL = os.path.join(os.path.dirname(__file__),
                             os.getenv('SQLITE_DB_NAME'))

CHUNK_SIZE = 1000
