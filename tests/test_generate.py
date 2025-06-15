from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate():
    payload = {
        "task_name": "extractive_summarization",
        "document": {
            "document_type": "transcription",
            "metadata": {},
            "content": "Patient John Doe visited NYC Hospital on January 5, 2023 due to high blood pressure."
        },
        "citation": False,
        "reasoning": False
    }
    response = client.post("/api/nextgen/generate", json=payload)
    assert response.status_code == 200
    assert "who" in response.json()
