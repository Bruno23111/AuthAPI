from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthorized_access():
    response = client.get("/api/tasks")  # Corrigido: /api/tasks em vez de /tasks
    assert response.status_code == 401
    assert "Authorization header missing" in response.json()["detail"]
