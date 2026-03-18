from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class Todo(TodoCreate):
    id: int
