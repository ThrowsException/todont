from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.database import create_db_and_tables
from app.routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(title="TODONT API", lifespan=lifespan)

mcp = FastApiMCP(app)
mcp.mount_http()

app.include_router(todos.router)

