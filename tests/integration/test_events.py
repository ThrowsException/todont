import pytest


@pytest.mark.integration
def test_create_produces_created_event(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "event test"}).json()["id"]
    cleanup_ids.append(todo_id)

    events = http_a.get(f"/events/todos/{todo_id}/events").json()
    assert len(events) >= 1
    assert events[0]["event_type"] == "TodoCreated"
    assert events[0]["payload"]["title"] == "event test"


@pytest.mark.integration
def test_mark_done_produces_event(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "done event"}).json()["id"]
    cleanup_ids.append(todo_id)
    http_a.patch(f"/todos/{todo_id}", json={"done": True})

    events = http_a.get(f"/events/todos/{todo_id}/events").json()
    event_types = [e["event_type"] for e in events]
    assert "TodoCreated" in event_types
    assert "TodoMarkedDone" in event_types


@pytest.mark.integration
def test_all_three_event_types(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "all events"}).json()["id"]
    cleanup_ids.append(todo_id)
    http_a.patch(f"/todos/{todo_id}", json={"done": True})
    http_a.patch(f"/todos/{todo_id}", json={"done": False})

    events = http_a.get(f"/events/todos/{todo_id}/events").json()
    event_types = [e["event_type"] for e in events]
    assert "TodoCreated" in event_types
    assert "TodoMarkedDone" in event_types
    assert "TodoMarkedUndone" in event_types


@pytest.mark.integration
def test_events_404_for_unknown_todo(http_a):
    r = http_a.get("/events/todos/00000000-0000-0000-0000-000000000000/events")
    assert r.status_code == 404


@pytest.mark.integration
def test_global_events_contains_created_todo(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "global event"}).json()["id"]
    cleanup_ids.append(todo_id)

    events = http_a.get("/events").json()
    assert any(e["todo_id"] == todo_id and e["event_type"] == "TodoCreated" for e in events)


@pytest.mark.integration
def test_global_events_limit(http_a, cleanup_ids):
    ids = [http_a.post("/todos", json={"title": f"limit {i}"}).json()["id"] for i in range(5)]
    cleanup_ids.extend(ids)

    events = http_a.get("/events", params={"limit": 3}).json()
    assert len(events) == 3


@pytest.mark.integration
def test_todo_events_requires_auth(app_url):
    import httpx
    r = httpx.get(f"{app_url}/events/todos/some-id/events")
    assert r.status_code == 401


@pytest.mark.integration
def test_global_events_requires_auth(app_url):
    import httpx
    r = httpx.get(f"{app_url}/events")
    assert r.status_code == 401
