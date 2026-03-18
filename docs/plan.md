# Implemented Plans

---

## Mark Todos as Done/Undone
**Date:** 2026-03-18

### Context
Todos had a `done` field but no way to toggle it after creation. Users needed an endpoint to transition a todo between done and undone states.

### Changes
- **`backend/app/models/todo.py`**: Added `TodoUpdate` model with `done: bool`; made `Todo` mutable via `ConfigDict(frozen=False)`
- **`backend/app/routers/todos.py`**: Added `PATCH /todos/{todo_id}` — looks up todo, mutates `done`, returns updated todo or 404
- **`tests/test_todos.py`**: Added `test_mark_todo_done`, `test_mark_todo_undone`, `test_mark_todo_not_found`
