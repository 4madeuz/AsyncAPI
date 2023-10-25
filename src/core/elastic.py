def get_elastic_query(index: str, page_number: int, page_size: int, **kwargs) -> dict:

    res_query = {
        'index': index,
        'from_': _get_offset(page_number, page_size),
        'size': page_size,
    }
    if kwargs['genre']:
        query = {
            'nested': {
                'path': 'genre',
                'query': {
                    'bool': {
                        'filter': {
                            'match': {'genre.uuid': kwargs['genre']}
                        }
                    }
                }
            }
        }
        res_query.setdefault('query', query)

    if kwargs['query']:
        query = {
            'match': {
                'title': {
                    'query': kwargs['query'],
                    'fuzziness': 'auto',
                }
            }
        }
        res_query.setdefault('query', query)

    if kwargs['sort']:
        split_sort_params = kwargs['sort'].split(',')
        res_query['sort'] = [_get_order(param) for param in split_sort_params]

    return res_query


def get_persons_query(index: str, page_number: int, page_size: int, **kwargs) ->  dict:

    res_query = {
        'index': index,
        'from_': _get_offset(page_number, page_size),
        'size': page_size,
    }

    if kwargs['persons_query']:
        query = {
            'match': {
                'full_name': {
                    'query': kwargs['persons_query'],
                    'fuzziness': 'auto',
                }
            }
        }
        res_query.setdefault('query', query)

    return res_query


def get_genres_query(index: str, page_number: int, page_size: int, **kwargs) ->  dict:

    res_query = {
        'index': index,
        'from_': _get_offset(page_number, page_size),
        'size': page_size,
    }

    if kwargs['genres_query']:
        query = {
            'match': {
                'name': {
                    'query': kwargs['genres_query'],
                    'fuzziness': 'auto',
                }
            }
        }
        res_query.setdefault('query', query)

    return res_query


def _get_order(sort: str) -> dict[str]:
    if sort.startswith('-'):
        return {sort[1:]: 'desc'}
    return {sort: 'asc'}


def _get_offset(page_number: int,  page_size: int) -> int:
    return page_number * page_size - page_size
