def test_create_todo_produces_event(client):
    response = client.post("/todos", json={"title": "Event test", "done": False})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    events = client.get(f"/events/todos/{todo_id}/events").json()
    assert len(events) == 1
    assert events[0]["event_type"] == "TodoCreated"
    assert events[0]["payload"]["title"] == "Event test"
    assert events[0]["payload"]["done"] is False


def test_mark_done_produces_event(client):
    todo_id = client.post("/todos", json={"title": "Mark done"}).json()["id"]
    client.patch(f"/todos/{todo_id}", json={"done": True})

    events = client.get(f"/events/todos/{todo_id}/events").json()
    assert len(events) == 2
    assert events[0]["event_type"] == "TodoCreated"
    assert events[1]["event_type"] == "TodoMarkedDone"


def test_mark_undone_produces_event(client):
    todo_id = client.post("/todos", json={"title": "Mark undone"}).json()["id"]
    client.patch(f"/todos/{todo_id}", json={"done": True})
    client.patch(f"/todos/{todo_id}", json={"done": False})

    events = client.get(f"/events/todos/{todo_id}/events").json()
    assert len(events) == 3
    assert events[0]["event_type"] == "TodoCreated"
    assert events[1]["event_type"] == "TodoMarkedDone"
    assert events[2]["event_type"] == "TodoMarkedUndone"


def test_todo_events_404_for_unknown_todo(client):
    response = client.get("/events/todos/9999/events")
    assert response.status_code == 404


def test_global_event_stream_returns_recent_events(client):
    id1 = client.post("/todos", json={"title": "Todo A"}).json()["id"]
    id2 = client.post("/todos", json={"title": "Todo B"}).json()["id"]

    events = client.get("/events").json()
    assert len(events) == 2
    # newest first
    assert events[0]["todo_id"] == id2
    assert events[1]["todo_id"] == id1


def test_global_event_stream_limit(client):
    for i in range(5):
        client.post("/todos", json={"title": f"Todo {i}"})

    events = client.get("/events?limit=3").json()
    assert len(events) == 3


def test_event_bus_handler_called_on_create(client):
    captured = []

    async def capture_handler(event):
        captured.append(event)

    from app.events import EventType, event_bus

    event_bus.subscribe(EventType.todo_created, capture_handler)

    client.post("/todos", json={"title": "Bus test"})

    assert len(captured) == 1
    assert captured[0].event_type == EventType.todo_created
