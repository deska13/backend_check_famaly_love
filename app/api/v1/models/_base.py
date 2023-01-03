from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class BaseAPIModel(BaseModel):
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
