import orjson


class RedisFormatter:

    @staticmethod
    def to_bytes(value: dict) -> bytes:
        return orjson.dumps(value)

    @staticmethod
    def to_dict(value: bytes) -> dict:
        return orjson.loads(value)
