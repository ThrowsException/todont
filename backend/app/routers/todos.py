from fastapi import APIRouter

router = APIRouter(prefix="/todos", tags=["todos"])

todos: list[dict] = []


@router.get("")
def read_all_todos():
    return todos


@router.post("")
def create_todo(todo: dict):
    todos.append(todo)
    return todo
