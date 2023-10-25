from time import sleep
from datetime import datetime


from etl import ETLState
from etl import config
from etl.utils import connectors
from etl.logs.logger import logger
from etl.etl_modules import extract, load, transform


def run_etl():
    pg_conn = connectors.get_connect_to_pg()
    extractor = extract.PostgresExtractor(pg_conn)
    transformer = transform.TransformToElastic()
    elastic = connectors.get_connect_to_elastic()
    loader = load.ElasticLoader(elastic)

    extracted_films = extractor.extract_films()
    for films in extracted_films:
        transformed_films = transformer.transform_films(films)

        logger.info('Transform {} films', len(transformed_films))
        loader.load_films_to_elastic(transformed_films)
        logger.info('Films successfully load')

    extracted_genres = extractor.extract_genres()
    for genres in extracted_genres:
        transformed_genres = transformer.transform_genres(genres)
        logger.info('Transform {} genres', len(transformed_genres))
        loader.load_genres_to_elastic(transformed_genres)
        logger.info('Genres successfully load')

    extracted_persons = extractor.extract_persons()
    for persons in extracted_persons:
        transformed_persons = transformer.transform_persons(persons)
        logger.info('Transform {} persons', len(transformed_persons))
        loader.load_persons_to_elastic(transformed_persons)
        logger.info('Persons successfully load')

    ETLState.set_state(config.general_settings.default_state_key, str(datetime.utcnow()))
    extractor.cursor.close()
    pg_conn.close()


if __name__ == '__main__':
    while True:
        logger.info('Start etl iteration')
        run_etl()
        sleep(config.general_settings.etl_sleep_time)
