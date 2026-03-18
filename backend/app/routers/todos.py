from fastapi import APIRouter

from backend.app.models.todo import Todo, TodoCreate

router = APIRouter(prefix="/todos", tags=["todos"])

todos: list[Todo] = []
_next_id: int = 1


@router.get("")
def read_all_todos() -> list[Todo]:
    return todos


@router.post("", status_code=201)
def create_todo(todo: TodoCreate) -> Todo:
    global _next_id
    new_todo = Todo(id=_next_id, **todo.model_dump())
    _next_id += 1
    todos.append(new_todo)
    return new_todo
