# Backend AGENTS.md

Python FastAPI app for the API.

## Running
```bash
uv run uvicorn backend.app.main:app --reload
```

## Linting
```bash
uv run ruff check backend/ tests/
uv run ruff check --fix backend/ tests/   # auto-fix
```

## Testing
```bash
uv run pytest -v                                    # all tests
uv run pytest tests/test_todos.py::test_name -v     # single test
```

Tests use FastAPI's `TestClient` (via httpx). Shared fixtures are in `tests/conftest.py`.