import uuid

from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth import verify_token
from app.database import get_session
from app.dynamo import get_table
from app.events import append_event, event_bus
from app.events.models import EventType
from app.models.todo import Todo, TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[Todo])
async def read_all_todos(
    table=Depends(get_table),
    token_payload: dict = Depends(verify_token),
):
    user_id = token_payload["sub"]
    result = table.query(
        IndexName="user_id-index",
        KeyConditionExpression=Key("user_id").eq(user_id),
    )
    return result.get("Items", [])


@router.post("", response_model=Todo, status_code=201)
async def create_todo(
    todo: TodoCreate,
    table=Depends(get_table),
    session: AsyncSession = Depends(get_session),
    token_payload: dict = Depends(verify_token),
):
    user_id = token_payload["sub"]
    todo_id = str(uuid.uuid7())
    item = {"id": todo_id, "title": todo.title, "done": todo.done, "user_id": user_id}
    table.put_item(Item=item)
    db_todo = Todo(id=todo_id, title=todo.title, done=todo.done)

    event = await append_event(
        session,
        todo_id,
        EventType.todo_created,
        {"title": db_todo.title, "done": db_todo.done},
    )
    await session.commit()
    await event_bus.publish(event)
    return db_todo


@router.patch("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: str,
    update: TodoUpdate,
    table=Depends(get_table),
    session: AsyncSession = Depends(get_session),
    token_payload: dict = Depends(verify_token),
):
    user_id = token_payload["sub"]
    response = table.get_item(Key={"id": todo_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Todo not found")
    if item.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    table.update_item(
        Key={"id": todo_id},
        UpdateExpression="SET #d = :done",
        ExpressionAttributeNames={"#d": "done"},
        ExpressionAttributeValues={":done": update.done},
    )
    item["done"] = update.done
    db_todo = Todo(id=item["id"], title=item["title"], done=item["done"])

    event_type = (
        EventType.todo_marked_done if update.done else EventType.todo_marked_undone
    )
    event = await append_event(session, todo_id, event_type, {"done": update.done})
    await session.commit()
    await event_bus.publish(event)
    return db_todo
