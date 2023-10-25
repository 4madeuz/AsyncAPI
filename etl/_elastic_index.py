from etl.logs.logger import logger
from etl.utils import connectors
from etl.queries_schemas.elastic import el_indexes


def create() -> None:
    logger.info('Create Elastic index')
    elastic_conn = connectors.get_connect_to_elastic()
    indexes = ['genres', 'movies', 'persons']
    for index in indexes:
        elastic_conn.indices.create(index=index, body=el_indexes[index])
        logger.info('Index {} successfully created', index)


if __name__ == '__main__':
    create()
