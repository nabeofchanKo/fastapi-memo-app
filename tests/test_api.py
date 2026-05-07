from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_memo():
    response = client.post("/memos", json={"title": "Test", "content": "Test content"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["content"] == "Test content"
    assert "id" in data
    assert "created_at" in data

def test_get_memos():
    response = client.get("/memos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_memo_not_found():
    response = client.get("/memos/999")
    assert response.status_code == 404

def test_update_memo():
    response = client.post("/memos", json={"title": "Test", "content": "Test content"})
    data = response.json()
    memo_id = data["id"]

    response = client.put(f"/memos/{memo_id}", json={"title": "Test Updated", "content": "Test content Updated"})
    data = response.json()
    assert data["title"] == "Test Updated"
    assert data["content"] == "Test content Updated"

def test_delete_memo():
    response = client.post("/memos", json={"title": "Test", "content": "Test content"})
    data = response.json()
    memo_id = data["id"]

    response = client.delete(f"/memos/{memo_id}")

    response = client.get(f"/memos/{memo_id}")
    assert response.status_code == 404