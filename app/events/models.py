from __future__ import annotations

import enum
from datetime import UTC, datetime
from typing import Any

from sqlmodel import JSON, Column, Field, SQLModel


class EventType(enum.StrEnum):
    todo_created = "TodoCreated"
    todo_marked_done = "TodoMarkedDone"
    todo_marked_undone = "TodoMarkedUndone"


class TodoEvent(SQLModel, table=True):
    __tablename__ = "todo_events"
    id: int | None = Field(default=None, primary_key=True)
    todo_id: str = Field(index=True, nullable=False)
    event_type: EventType = Field(nullable=False)
    payload: dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
