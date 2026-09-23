"""
tests/test_api.py
Automated API Verification for EndpointShield AI
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_invalid_payload():
    # Pass 10 features instead of required 512
    response = client.post("/scan-binary", json={"features": [0.1] * 10})
    assert response.status_code == 400
