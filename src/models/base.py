import orjson
from pydantic import BaseModel, UUID4

from src.core.common import orjson_dumps


class Model(BaseModel):
    uuid: UUID4

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ListModel(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
