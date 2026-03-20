# Implemented Plans

---

## Mark Todos as Done/Undone
**Date:** 2026-03-18

### Context
Todos had a `done` field but no way to toggle it after creation. Users needed an endpoint to transition a todo between done and undone states.

### Changes
- **`app/models/todo.py`**: Added `TodoUpdate` model with `done: bool`; made `Todo` mutable via `ConfigDict(frozen=False)`
- **`app/routers/todos.py`**: Added `PATCH /todos/{todo_id}` — looks up todo, mutates `done`, returns updated todo or 404
- **`tests/test_todos.py`**: Added `test_mark_todo_done`, `test_mark_todo_undone`, `test_mark_todo_not_found`

---

## Add SQLite Database Persistence
**Date:** 2026-03-19

### Context
The app used an in-memory list (`todos: list[Todo] = []`) that was lost on every restart. Replaced with a persistent SQLite file-based database using SQLModel and aiosqlite.

### Changes
- **`app/database.py`** (new): Central DB config — async engine, session factory, `create_db_and_tables()`, and `get_session()` FastAPI dependency
- **`app/models/todo.py`**: Rewrote using SQLModel — `TodoBase`, `Todo(table=True)` with auto-increment PK, `TodoCreate`, `TodoUpdate`
- **`app/routers/todos.py`**: Removed in-memory list and `_next_id`; all endpoints now `async` and use `session: AsyncSession = Depends(get_session)`
- **`app/main.py`**: Added `lifespan` context manager to call `create_db_and_tables()` on startup
- **`tests/conftest.py`**: Rewrote fixture to use in-memory SQLite per test, patching `app.database` module globals for full isolation
- **`.gitignore`**: Added `todos.db`
