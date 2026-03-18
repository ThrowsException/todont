import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import todos as todos_module


@pytest.fixture
def client():
    todos_module.todos.clear()
    todos_module._next_id = 1
    return TestClient(app)
