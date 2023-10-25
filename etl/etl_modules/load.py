from elasticsearch import helpers
from dataclasses import asdict

from etl import models
from etl.logs.logger import logger


class ElasticLoader:

    def __init__(self, elastic):
        self.elastic = elastic

    def load_films_to_elastic(self, films: list[models.ElasticFilmRecord]) -> None:
        rows = [
            {
                '_index': 'movies',
                '_id': row.uuid,
                '_source': asdict(row)
            }
            for row in films
        ]
        helpers.bulk(self.elastic, rows)
        logger.info('Load {} rows', len(rows))

    def load_genres_to_elastic(self, genres: list[models.ElasticGenreRecord]):
        rows = [
            {
                '_index': 'genres',
                '_id': row.uuid,
                '_source': asdict(row)
            }
            for row in genres
        ]
        helpers.bulk(self.elastic, rows)
        logger.info('Load {} rows', len(rows))

    def load_persons_to_elastic(self,  persons: list[models.ElasticPersonRecord]):
        rows = [
            {
                '_index': 'persons',
                '_id': row.uuid,
                '_source': asdict(row)
            }
            for row in persons
        ]
        helpers.bulk(self.elastic, rows)
        logger.info('Load {} rows', len(rows))
