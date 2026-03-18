def test_read_all_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    todo = {"title": "Test todo", "done": False}
    response = client.post("/todos", json=todo)
    assert response.status_code == 200
    assert response.json() == todo


def test_create_and_list_todo(client):
    todo = {"title": "Another todo", "done": False}
    client.post("/todos", json=todo)
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert any(t["title"] == "Another todo" for t in todos)
