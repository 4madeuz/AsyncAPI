import os
from pathlib import Path
from pydantic import BaseSettings, Field

PROJECT_NAME = 'Async Api'

_PATH_TO_ENV = os.path.join(Path(__file__).parent.parent, '.env.test') if os.getenv('TEST') == 'True' else \
    os.path.join(Path(__file__).parent.parent, '.env')


class BaseConfig(BaseSettings):
    class Config:
        env_file = _PATH_TO_ENV
        env_file_encoding = 'utf-8'


class RedisCredentials(BaseConfig):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')
    decode_responses: bool = True


class ESCredentials(BaseConfig):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')


class ApiSettings(BaseSettings):
    project_name: str = 'Async API for cinema'
    redis_keys_expiration = 60 * 5
    redis: RedisCredentials = RedisCredentials()
    elastic: ESCredentials = ESCredentials()


settings = ApiSettings()
