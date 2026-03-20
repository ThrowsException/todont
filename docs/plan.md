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

---

## Event-Driven Architecture with Event Sourcing
**Date:** 2026-03-19

### Context
The app stored only current state with no audit trail or history. Introduced event sourcing so every state change is recorded as an immutable event, with the `Todo` table becoming a derived projection. Added an in-process event bus to decouple side-effects from command logic.

### Changes
- **`app/events/models.py`** (new): `TodoEvent` SQLModel table and `EventType` enum (`TodoCreated`, `TodoMarkedDone`, `TodoMarkedUndone`)
- **`app/events/store.py`** (new): `append_event` (no commit — caller owns transaction), `get_events_for_todo`, `get_recent_events`
- **`app/events/bus.py`** (new): `EventBus` class with `subscribe`/`publish`; errors in handlers are logged and isolated via `return_exceptions=True`; `event_bus` singleton
- **`app/events/__init__.py`** (new): Re-exports all key symbols
- **`app/routers/todos.py`**: Updated `create_todo` to `flush()` before event (to get ID), then `append_event` + atomic `commit` + `publish`; same pattern for `update_todo`
- **`app/routers/events.py`** (new): `GET /events/todos/{todo_id}/events` (ordered history, 404 if missing) and `GET /events?limit=N` (global stream, newest first, limit 1–500)
- **`app/main.py`**: Added `events_router`, registered `log_todo_created` audit handler on `EventType.todo_created` in lifespan
- **`tests/conftest.py`**: Added `autouse` fixture to clear `event_bus._handlers` between tests
- **`tests/test_events.py`** (new): 7 tests covering event creation, ordering, 404 handling, stream limits, and bus dispatch

### Key Design Decisions
- `id`-based event ordering (not `occurred_at`) — two events in the same millisecond stay ordered
- `payload` is untyped JSON — different event types carry different fields; maps to PostgreSQL `jsonb` with zero schema change
- No FK on `todo_id` — event log stays intact if todos are archived/sharded
- `append_event` does not commit — router commits once so event + projection update are atomic
