import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core import APISetting


api_setting = APISetting(_env_file='config/api.env')


app = FastAPI(
    title="Check famaly love",
    description="Бэкенд check famaly love",
    version="0.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=api_setting.allow_origins,
    allow_credentials=api_setting.allow_credentials,
    allow_methods=api_setting.allow_methods,
    allow_headers=api_setting.allow_headers,
)


app.include_router(
    api_router
)


if __name__ == "__main__":
    uvicorn.run("main:app", host=api_setting.server_host, port=api_setting.server_port, reload=True)
