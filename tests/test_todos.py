def test_read_all_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    todo = {"title": "Test todo", "done": False}
    response = client.post("/todos", json=todo)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["done"] is False
    assert "id" in data


def test_create_and_list_todo(client):
    todo = {"title": "Another todo", "done": False}
    client.post("/todos", json=todo)
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert any(t["title"] == "Another todo" for t in todos)


def test_mark_todo_done(client):
    create_response = client.post("/todos", json={"title": "Mark me done"})
    todo_id = create_response.json()["id"]
    response = client.patch(f"/todos/{todo_id}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_mark_todo_undone(client):
    create_response = client.post("/todos", json={"title": "Mark me undone"})
    todo_id = create_response.json()["id"]
    client.patch(f"/todos/{todo_id}", json={"done": True})
    response = client.patch(f"/todos/{todo_id}", json={"done": False})
    assert response.status_code == 200
    assert response.json()["done"] is False


def test_mark_todo_not_found(client):
    response = client.patch("/todos/9999", json={"done": True})
    assert response.status_code == 404


def test_get_todos_only_returns_own(client):
    from app.auth import verify_token
    from app.main import app
    from tests.conftest import _stub_verify_token

    client.post("/todos", json={"title": "test-user todo"})

    async def other_user():
        return {"sub": "other-user"}

    app.dependency_overrides[verify_token] = other_user
    response = client.get("/todos")
    assert response.json() == []
    app.dependency_overrides[verify_token] = _stub_verify_token


def test_patch_other_users_todo_returns_403(client):
    from app.auth import verify_token
    from app.main import app
    from tests.conftest import _stub_verify_token

    create_resp = client.post("/todos", json={"title": "Mine"})
    todo_id = create_resp.json()["id"]

    async def other_user():
        return {"sub": "other-user"}

    app.dependency_overrides[verify_token] = other_user
    response = client.patch(f"/todos/{todo_id}", json={"done": True})
    assert response.status_code == 403
    app.dependency_overrides[verify_token] = _stub_verify_token
