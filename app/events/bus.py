import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable

from app.events.models import EventType, TodoEvent

EventHandler = Callable[[TodoEvent], Awaitable[None]]


class EventBus:
    def __init__(self):
        self._handlers: dict[EventType, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: TodoEvent) -> None:
        """Call AFTER commit. Errors in handlers are logged, not re-raised."""
        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            return
        results = await asyncio.gather(
            *(h(event) for h in handlers), return_exceptions=True
        )
        for handler, result in zip(handlers, results):
            if isinstance(result, Exception):
                logging.getLogger(__name__).error(
                    "Handler %s failed for event %s: %s",
                    handler.__name__,
                    event.id,
                    result,
                )


event_bus = EventBus()
