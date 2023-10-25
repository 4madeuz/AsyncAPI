from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import genres
from src.api.v1 import films
from src.api.v1 import persons
from src.core import config
from src.db import elastic, redis

app = FastAPI(
    title=config.ApiSettings().project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=config.settings.redis.host, port=config.settings.redis.port)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.settings.elastic.host}:{config.settings.elastic.port}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
