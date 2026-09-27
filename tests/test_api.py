"""
tests/test_api.py
Automated API Verification for EndpointShield AI
"""
import sys
import os

# Dynamically add the root directory (ML-Final-Lab-Group-04) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_predict_endpoint():
    # Test payload containing 512 static features matching Noel's schema
    payload = {"features": [0.0] * 512}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "malware_probability" in response.json()
    assert "status" in response.json()
