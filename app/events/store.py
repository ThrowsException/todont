from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.events.models import EventType, TodoEvent


async def append_event(
    session: AsyncSession, todo_id: int, event_type: EventType, payload: dict
) -> TodoEvent:
    """Does NOT commit — caller owns the transaction boundary."""
    event = TodoEvent(todo_id=todo_id, event_type=event_type, payload=payload)
    session.add(event)
    await session.flush()  # assigns event.id without committing
    return event


async def get_events_for_todo(session: AsyncSession, todo_id: int) -> list[TodoEvent]:
    result = await session.exec(
        select(TodoEvent).where(TodoEvent.todo_id == todo_id).order_by(TodoEvent.id)
    )
    return list(result.all())


async def get_recent_events(session: AsyncSession, limit: int = 50) -> list[TodoEvent]:
    result = await session.exec(
        select(TodoEvent).order_by(TodoEvent.id.desc()).limit(limit)
    )
    return list(result.all())
