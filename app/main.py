import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.database import create_db_and_tables
from app.events import EventType, event_bus
from app.routers import events as events_router
from app.routers import todos


async def log_todo_created(event):
    logging.getLogger("audit").info("TodoCreated: todo_id=%s", event.todo_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    event_bus.subscribe(EventType.todo_created, log_todo_created)
    yield


app = FastAPI(title="TODONT API", lifespan=lifespan)

mcp = FastApiMCP(app)
mcp.mount_http()

app.include_router(todos.router)
app.include_router(events_router.router)
