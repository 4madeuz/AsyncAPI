class ElasticQuery:

    __FULLTEXT_SEARCH_FIELD_MAPPER = {
        'movies': 'title',
        'persons': 'full_name',
    }

    def __init__(
            self,
            index: str,
            **kwargs
    ):
        self._queries = kwargs
        self._fulltext_search_field = self.__FULLTEXT_SEARCH_FIELD_MAPPER.get(index)
        self._query = {
            'index': index,
        }
        self.__add_pagination()

    def get_query(self):
        query_mapper = {
            'query': self._add_query,
            'genre': self._add_genre,
            'sort': self._add_sort,
        }

        for q_name, q_handler in query_mapper.items():
            query_value = self._queries.get(q_name)

            if query_value is not None:
                q_handler(query_value)

        return self._query

    def __add_pagination(self):
        page_number = self._queries.get('page_number')
        page_size = self._queries.get('page_size')
        if page_number is not None and page_size is not None:
            self._query['from_'] = _get_offset(page_number, page_size)
            self._query['size'] = page_size

    def _add_query(self, query):

        res_query = {
            'match': {
                self._fulltext_search_field: {
                    'query': query,
                    'fuzziness': 'auto',
                }
            }
        }
        self._query.setdefault('query', res_query)

    def _add_genre(self, genre):
        if not genre:
            return self

        res_query = {
            'nested': {
                'path': 'genre',
                'query': {
                    'bool': {
                        'filter': {
                            'match': {'genre.uuid': genre}
                        }
                    }
                }
            }
        }
        self._query.setdefault('query', res_query)
        return self

    def _add_sort(self, sort: str):
        if not sort:
            return self

        splited_sort_params = sort.split(',')
        self._query['sort'] = [_get_order(param) for param in splited_sort_params]
        return self


def _get_order(sort: str) -> dict[str]:
    if sort.startswith('-'):
        return {sort[1:]: 'desc'}
    return {sort: 'asc'}


def _get_offset(page_number: int,  page_size: int) -> int:
    return page_number * page_size - page_size
