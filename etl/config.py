import os.path

from pydantic import BaseSettings, Field
from pathlib import Path


class BaseConfig(BaseSettings):

    class Config:
        env_file = os.path.join(Path(__file__).parent, '.env')
        env_file_encoding = 'utf-8'


class DatabaseSettings(BaseConfig):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')


class RedisSettings(BaseConfig):
    host: str = Field(..., env='REDIS_HOST')
    port: str = Field(..., env='REDIS_PORT')
    decode_responses: bool = True


class ElasticSearchSettings(BaseConfig):
    host: str = Field(..., env='ELASTIC_HOST')
    port: str = Field(..., env='ELASTIC_PORT')


class GeneralSettings(BaseSettings):
    base_dir: Path = Path(__file__).parent
    logs_path: str = os.path.join(base_dir, 'logs/logs.log')
    butch_size: int = 200
    default_state_key: str = 'modified'
    etl_sleep_time: int = 10


def get_postgres_credentials():
    return {
        'dbname': database_settings.dbname,
        'user': database_settings.user,
        'password': database_settings.password,
        'host': database_settings.host,
        'port': database_settings.port,
    }


database_settings = DatabaseSettings()
general_settings = GeneralSettings()
redis_settings = RedisSettings()
elasticsearch_settings = ElasticSearchSettings()
