import os
from pathlib import Path
from uuid import uuid4

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(Path(__file__).parent, '.env')
        env_file_encoding = 'utf-8'


class TestSettings(BaseConfig):
    es_host: str = Field(..., env='ELASTIC_HOST')
    es_port: int = Field(..., env='ELASTIC_PORT')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    es_film_index = 'movies'

    es_genre_index = 'genres'

    es_person_index = 'persons'

    indexes = ['genres', 'movies', 'persons']

    service_url: str = 'http://api_test:8000'


test_settings = TestSettings()
