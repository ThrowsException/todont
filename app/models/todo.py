from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    done: bool = False


class Todo(TodoBase):
    id: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    done: bool
