from typing import Optional, List

from pydantic import BaseSettings


class APISetting(BaseSettings):
    server_host: str
    server_port: int
    
    allow_origins: List[str]
    allow_credentials: bool
    allow_methods: List[str]
    allow_headers: List[str]
