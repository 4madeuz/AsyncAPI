import backoff
from redis import Redis, ConnectionError

from tests.functional.utils.loaders.base import Loader
from tests.functional.settings import test_settings
from tests.functional.utils.loaders.logger import backoff_logger


_EXCEPTIONS = (ConnectionError,)


class RedisLoader(Loader):

    def __init__(self):
        self.client = Redis(host=test_settings.redis_host, port=test_settings.redis_port)

    @backoff.on_exception(
        backoff.expo,
        _EXCEPTIONS,
        logger=backoff_logger
    )
    def post_connection(self) -> None:
        connect = self.client.ping
        if connect:
            return
