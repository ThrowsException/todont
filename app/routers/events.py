from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.dynamo import get_table
from app.events import get_events_for_todo, get_recent_events
from app.events.models import TodoEvent

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/todos/{todo_id}/events", response_model=list[TodoEvent])
async def read_todo_events(
    todo_id: str,
    table=Depends(get_table),
    session: AsyncSession = Depends(get_session),
):
    response = table.get_item(Key={"id": todo_id})
    if not response.get("Item"):
        raise HTTPException(status_code=404, detail="Todo not found")
    return await get_events_for_todo(session, todo_id)


@router.get("", response_model=list[TodoEvent])
async def read_recent_events(
    limit: int = Query(default=50, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
):
    return await get_recent_events(session, limit)
