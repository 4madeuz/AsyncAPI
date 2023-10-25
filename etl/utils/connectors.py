from typing import NoReturn

import psycopg2
from elasticsearch import Elasticsearch, ConnectionError
from psycopg2.extras import DictCursor

from etl import config
from etl.utils.back_off import back_off


@back_off()
def get_connect_to_pg():
    with psycopg2.connect(**config.get_postgres_credentials(),
                          cursor_factory=DictCursor) as conn:
        return conn


@back_off()
def get_connect_to_elastic() -> Elasticsearch | NoReturn:
    elastic_url = 'http://{host}:{port}'.format(
        host=config.elasticsearch_settings.host,
        port=config.elasticsearch_settings.port
    )
    elastic = Elasticsearch(hosts=elastic_url)
    if not elastic.ping():
        raise ConnectionError('Error')
    return elastic
