import redis as _redis

from etl.config import redis_settings


REDIS_CONN = {
    'host': redis_settings.host,
    'port': redis_settings.port,
    'decode_responses': True,
}

redis = _redis.Redis(**REDIS_CONN)


class BaseStorage:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            instance = super().__new__(cls, *args, **kwargs)
            cls.__instance = instance
            return instance
        return cls.__instance

    def __init__(self, instance):
        self.instance = instance


class RedisStorage(BaseStorage):

    def __init__(self, storage=redis):
        super().__init__(storage)


class ETLState:
    storage = RedisStorage()

    def get_state(self, key):
        return self.storage.instance.get(key)

    def set_state(self, key, value):
        self.storage.instance.set(key, value)
