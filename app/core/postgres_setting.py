from typing import Optional

from pydantic import BaseSettings


class PostgresSetting(BaseSettings):
    postgres_sync_connect: Optional[str]
    postgres_async_connect: str

    class Config:
        env_file = "config/postgres.env"