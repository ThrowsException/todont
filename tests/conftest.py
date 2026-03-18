import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routers.todos import todos


@pytest.fixture
def client():
    todos.clear()
    return TestClient(app)
