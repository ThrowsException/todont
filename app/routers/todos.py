from fastapi import APIRouter, HTTPException

from app.models.todo import Todo, TodoCreate, TodoUpdate

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


@router.patch("/{todo_id}")
def update_todo(todo_id: int, update: TodoUpdate) -> Todo:
    for todo in todos:
        if todo.id == todo_id:
            todo.done = update.done
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
