from time import sleep
from functools import wraps

import psycopg2
import elastic_transport

from etl.logs.logger import logger


def back_off(start_sleep_time=0.1, factor=2, border_sleep_time=10):

    def wrapper(db_connection):
        counter = 1

        @wraps(db_connection)
        def inner(*args, **kwargs):
            nonlocal counter
            sleep_time = None

            while True:

                try:
                    return db_connection(*args, **kwargs)
                except psycopg2.OperationalError:
                    logger.critical(
                        'An error occurred during connection establishment with Postgres'
                    )
                except elastic_transport.ConnectionError:
                    logger.critical(
                        'An error occurred during connection establishment with ElasticSearch'
                    )

                if not sleep_time:
                    sleep(start_sleep_time)
                    sleep_time = start_sleep_time * factor ** counter
                    counter += 1
                    continue

                sleep_time = min(start_sleep_time * factor ** counter, border_sleep_time)
                logger.info('Trying to reconnect through {}s.', sleep_time)
                sleep(sleep_time)
                counter += 1
        return inner
    return wrapper
