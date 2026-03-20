from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

import app.database as db_module
from app.database import get_session
from app.main import app


@pytest.fixture
def client():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    test_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    original_engine = db_module.engine
    original_factory = db_module.async_session_factory
    db_module.engine = test_engine
    db_module.async_session_factory = test_factory

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        async with test_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    db_module.engine = original_engine
    db_module.async_session_factory = original_factory


@pytest.fixture(autouse=True)
def clear_event_bus():
    yield
    from app.events import event_bus

    event_bus._handlers.clear()
