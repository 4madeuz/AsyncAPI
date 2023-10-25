import backoff
from elasticsearch import Elasticsearch
from elasticsearch import ApiError, TransportError

from tests.functional.settings import test_settings
from tests.functional.testdata import elastic_index
from tests.functional.testdata import elastic_data
from tests.functional.utils.loaders.base import Loader
from tests.functional.utils.loaders.logger import backoff_logger

_EXCEPTIONS = ApiError, TransportError


class ElasticLoader(Loader):

    def __init__(self):
        self.client = Elasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}')

    @backoff.on_exception(
        backoff.expo,
        _EXCEPTIONS,
        logger=backoff_logger,
    )
    def post_connection(self) -> None:
        for index in test_settings.indexes:
            if self._is_index_exists(index):
                return

            self.client.indices.create(index=index, body=elastic_index.el_indexes[index])

            if self.client.count(index=index)['count'] < elastic_data.RECORDS_COUNT:
                bulk_query = []
                for row in elastic_data.TEST_DATA[index]:
                    bulk_query.extend([
                        {'index': {'_index': index, '_id': row['uuid']}},
                        row
                    ])
                response = self.client.bulk(operations=bulk_query)

                if response['errors']:
                    raise Exception('Ошибка записи данных в Elasticsearch')

    def _is_index_exists(self, index: str) -> bool:
        return self.client.indices.exists(index=index, body=elastic_index.el_indexes[index])
