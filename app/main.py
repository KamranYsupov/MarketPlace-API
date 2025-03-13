from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from app.core.config import settings
from app.core.container import Container, container
from app.api.v1 import routers
from app.db import Base, db_manager

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):

    yield

    await db_manager.dispose()


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app.container = container
    fastapi_app.include_router(routers.api_router, prefix=settings.api_v1_prefix)



    return fastapi_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app='app.main:app', reload=True)
