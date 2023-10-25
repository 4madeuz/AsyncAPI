import uuid


RECORDS_COUNT = 100

TEST_DATA = {
    'movies':  [{
        'uuid': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [
            {'uuid': str(uuid.uuid4()), 'name': 'Action'},
            {'uuid': str(uuid.uuid4()), 'name': 'Sci-Fi'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'uuid': str(uuid.uuid4()), 'full_name': 'Ann'},
            {'uuid': str(uuid.uuid4()), 'full_name': 'Bob'}
        ],
        'writers': [
            {'uuid': str(uuid.uuid4()), 'full_name': 'Ben'},
            {'uuid': str(uuid.uuid4()), 'full_name': 'Howard'}
        ],
        'directors': [
            {'uuid': str(uuid.uuid4()), 'full_name': 'Stan'}
        ],
        } for _ in range(RECORDS_COUNT)],

    'genres': [{
            'uuid': str(uuid.uuid4()),
            'name': 'Action',
        } for _ in range(RECORDS_COUNT)],


    'persons': [{
            'uuid': str(uuid.uuid4()),
            'full_name': 'Mark Hamill',
            'actors': [
                {'uuid': str(uuid.uuid4()), 'title': 'Star Slammer'},
                {'uuid': str(uuid.uuid4()), 'title': 'Star Slammer'}
            ],
            'writers': [
                {'uuid': str(uuid.uuid4()), 'title': 'Star Slammer'},
                {'uuid': str(uuid.uuid4()), 'title': 'Star Slammer'}
            ],
            'directors': [
                {'uuid': str(uuid.uuid4()), 'title': 'Star Slammer'}
            ],
        } for _ in range(RECORDS_COUNT)]
}
