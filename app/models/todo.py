from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class Todo(TodoCreate):
    model_config = ConfigDict(frozen=False)

    id: int


class TodoUpdate(BaseModel):
    done: bool
