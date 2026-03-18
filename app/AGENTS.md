# App AGENTS.md

Python FastAPI app for the API.

## Running
```bash
fastapi dev app/main.py
```

## Linting
```bash
uv run ruff check app/ tests/
uv run ruff check --fix app/ tests/   # auto-fix
```

## Testing
```bash
uv run pytest -v                                    # all tests
uv run pytest tests/test_todos.py::test_name -v     # single test
```

Tests use FastAPI's `TestClient` (via httpx). Shared fixtures are in `tests/conftest.py`.