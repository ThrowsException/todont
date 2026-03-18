import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/todos", tags=["todos"])

todos = []


@router.get("")
def read_all_todos():
    return JSONResponse(content=json.dumps(todos), media_type="application/json")


@router.post("")
def create_todo(todo: dict):
    todos.append(todo)
    return JSONResponse(content=json.dumps(todo), media_type="application/json")
