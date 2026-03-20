from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.todo import Todo, TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[Todo])
async def read_all_todos(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Todo))
    return result.all()


@router.post("", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate, session: AsyncSession = Depends(get_session)):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo


@router.patch("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int, update: TodoUpdate, session: AsyncSession = Depends(get_session)
):
    db_todo = await session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.done = update.done
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo
