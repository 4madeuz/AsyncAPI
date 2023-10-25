from loguru import logger
from etl import config

LOGGER = logger.add(
    sink=config.general_settings.logs_path,
    level='INFO',
)
