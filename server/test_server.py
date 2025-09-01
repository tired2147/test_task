import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.app import app
from server.database import Base, gget_db

SQLITE_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLITE_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[gget_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)
#ТЕСТ 1:создание записи
def test_create_click_data_success(test_db):
   
    response = client.post(
        "/api/clicks/",
        json={"text": "Test text", "click_count": 1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test text"
    assert data["click_count"] == 1
    assert "id" in data
    assert "created_at" in data
#ТЕСТ 2: Получение данных 
def test_get_click_history_with_pagination(test_db):
   
    # Создаем несколько записей
    for i in range(5):
        client.post(
            "/api/clicks/",
            json={"text": f"Test {i}", "click_count": i + 1}
        )
    
    response = client.get("/api/click-history/?page=1&size=3")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["size"] == 3
    assert data["pages"] == 2
#ТЕСТ 3:пробуем запросить  запрещенные методы
def test_method_not_allowed_for_wrong_http_methods(test_db):
    
    # GET на POST эндпоинт
    response = client.get("/api/clicks/")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"
    
    # POST на GET эндпоинт
    response = client.post("/api/click-history/")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"