import pytest


@pytest.mark.integration
def test_create_todo(http_a, cleanup_ids):
    r = http_a.post("/todos", json={"title": "integration test todo"})
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["title"] == "integration test todo"
    assert data["done"] is False
    cleanup_ids.append(data["id"])


@pytest.mark.integration
def test_created_todo_appears_in_list(http_a, cleanup_ids):
    r = http_a.post("/todos", json={"title": "listed todo"})
    assert r.status_code == 201
    todo_id = r.json()["id"]
    cleanup_ids.append(todo_id)

    todos = http_a.get("/todos").json()
    assert any(t["id"] == todo_id for t in todos)


@pytest.mark.integration
def test_list_todos_requires_auth(app_url):
    r = pytest.importorskip("httpx").get(f"{app_url}/todos")
    assert r.status_code == 401


@pytest.mark.integration
def test_create_todo_requires_auth(app_url):
    import httpx
    r = httpx.post(f"{app_url}/todos", json={"title": "no auth"})
    assert r.status_code == 401


@pytest.mark.integration
def test_mark_todo_done(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "mark done"}).json()["id"]
    cleanup_ids.append(todo_id)

    r = http_a.patch(f"/todos/{todo_id}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True


@pytest.mark.integration
def test_mark_todo_undone(http_a, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "mark undone"}).json()["id"]
    cleanup_ids.append(todo_id)

    http_a.patch(f"/todos/{todo_id}", json={"done": True})
    r = http_a.patch(f"/todos/{todo_id}", json={"done": False})
    assert r.status_code == 200
    assert r.json()["done"] is False


@pytest.mark.integration
def test_patch_todo_not_found(http_a):
    r = http_a.patch("/todos/00000000-0000-0000-0000-000000000000", json={"done": True})
    assert r.status_code == 404


@pytest.mark.integration
def test_patch_requires_auth(http_a, app_url, cleanup_ids):
    import httpx

    todo_id = http_a.post("/todos", json={"title": "auth patch test"}).json()["id"]
    cleanup_ids.append(todo_id)

    r = httpx.patch(f"{app_url}/todos/{todo_id}", json={"done": True})
    assert r.status_code == 401


@pytest.mark.integration
def test_list_only_shows_own_todos(http_a, http_b, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "user a private todo"}).json()["id"]
    cleanup_ids.append(todo_id)

    todos_b = http_b.get("/todos").json()
    assert not any(t["id"] == todo_id for t in todos_b)


@pytest.mark.integration
def test_patch_other_users_todo_returns_403(http_a, http_b, cleanup_ids):
    todo_id = http_a.post("/todos", json={"title": "user a todo"}).json()["id"]
    cleanup_ids.append(todo_id)

    r = http_b.patch(f"/todos/{todo_id}", json={"done": True})
    assert r.status_code == 403
