from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_capabilities():
    response = client.get("/api/nextgen/capabilities")
    assert response.status_code == 200
    assert "models" in response.json()
