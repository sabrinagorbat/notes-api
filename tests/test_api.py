import pytest
from app import create_app, db
from app.models import Note

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_create_note(client):
    response = client.post("/api/notes", json={
        "title": "Test Note",
        "content": "Test Content",
        "category": "test"
    })
    assert response.status_code == 201

def test_get_notes(client):
    client.post("/api/notes", json={"title": "Test", "content": "Content"})
    response = client.get("/api/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"]

def test_delete_note(client):
    resp = client.post("/api/notes", json={"title": "Delete Me", "content": "Content"})
    note_id = resp.get_json()["id"]
    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

def test_create_tag(client):
    response = client.post("/api/tags", json={"name": "test-tag"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "test-tag"


def test_get_tags(client):
    client.post("/api/tags", json={"name": "tag1"})
    client.post("/api/tags", json={"name": "tag2"})
    response = client.get("/api/tags")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] >= 2


def test_add_tag_to_note(client):
    resp = client.post("/api/notes", json={"title": "Note", "content": "Content"})
    note_id = resp.get_json()["id"]
    response = client.post(f"/api/notes/{note_id}/tags", json={"name": "my-tag"})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["tags"]) >= 1