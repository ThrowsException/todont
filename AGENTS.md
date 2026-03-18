# AGENTS.md

This project is a todo application. The main goal is to learn agentic coding and interacting with code agents.

## Instructions

- Aftering implementing a plan append the summary to docs/plan.md or make a bespoke plan file
  
## Project Structure
```
backend/         # FastAPI backend
  app/
    main.py      # App entry point
    routers/     # API route modules
    models/      # Data models
frontend/        # Future frontend (placeholder)
```

## Dev environment tips
- activate virtualenvironemtn with `source ./.venv/bin/activate` 
- to add packages `uv add <package>`
- Run backend: `uv run uvicorn backend.app.main:app --reload`
- Lint: `uv run ruff check backend/ tests/`
- Lint fix: `uv run ruff check --fix backend/ tests/`
- Test: `uv run pytest -v`
- Test single: `uv run pytest tests/test_todos.py::test_name -v`

## Technology

Technology used for the project

### Languages
- Python

### Libraries
- FastAPI
- Uvicorn
- Ruff (linting)
- Pytest + httpx (testing)

### Containers
- Docker
