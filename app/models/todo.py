
from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str
    done: bool = False


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    done: bool
