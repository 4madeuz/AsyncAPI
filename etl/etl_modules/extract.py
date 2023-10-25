from datetime import datetime

from etl import config, ETLState
from etl.queries_schemas import sql
from etl.logs.logger import logger


class PostgresExtractor:

    def __init__(self, connect, batch_size: int = config.general_settings.butch_size):
        self.cursor = connect.cursor()
        self.butch_size = batch_size

    def extract_films(self):
        state, format_date = self._get_state_and_format_date()
        self.cursor.execute(sql.sql_queries['films'], (
            tuple([(datetime.strptime(str(state), format_date))])
        ) * 3)

        while records := self.cursor.fetchmany(self.butch_size):
            logger.info('Updated and retrieved: {} film rows', len(records))
            yield records

    def extract_genres(self):
        state, format_date = self._get_state_and_format_date()
        self.cursor.execute(sql.sql_queries['genres'], (
            tuple([datetime.strptime(str(state), format_date)])
        ))

        while records := self.cursor.fetchmany(self.butch_size):
            logger.info('Updated and retrieved: {} genre rows', len(records))
            yield records

    def extract_persons(self):
        state, format_date = self._get_state_and_format_date()
        self.cursor.execute(sql.sql_queries['persons'], (
            tuple([datetime.strptime(str(state), format_date)])
        ))

        while records := self.cursor.fetchmany(self.butch_size):
            logger.info('Updated and retrieved: {} person rows', len(records))
            yield records

    @staticmethod
    def _get_state_and_format_date():
        state = ETLState.get_state(config.general_settings.default_state_key)
        format_date = '%Y-%m-%d %H:%M:%S.%f'
        if not state:
            state = datetime.min
            format_date = '%Y-%m-%d %H:%M:%S'

        return state, format_date
