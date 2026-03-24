import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi_mcp import AuthConfig, FastApiMCP

from app.auth import verify_token
from app.database import create_db_and_tables
from app.events import EventType, event_bus
from app.routers import events as events_router
from app.routers import todos

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")


async def log_todo_created(event):
    logging.getLogger("audit").info("TodoCreated: todo_id=%s", event.todo_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    event_bus.subscribe(EventType.todo_created, log_todo_created)
    yield


app = FastAPI(title="TODONT API", lifespan=lifespan)

_keycloak_client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
_auth_config = (
    AuthConfig(
        dependencies=[Depends(verify_token)],
        issuer=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}",
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret=_keycloak_client_secret,
        setup_proxies=True,
        setup_fake_dynamic_registration=True,
    )
    if _keycloak_client_secret
    else None
)

mcp = FastApiMCP(app, auth_config=_auth_config)
mcp.mount_http()

app.include_router(todos.router, dependencies=[Depends(verify_token)])
app.include_router(events_router.router, dependencies=[Depends(verify_token)])
