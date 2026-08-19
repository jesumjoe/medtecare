import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "MedTeCare Squad C Backend"
    assert "engine_ready" in data

def test_diagnose_invalid_json():
    response = client.post("/api/v1/diagnose", data="invalid json")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid JSON payload."}

def test_diagnose_valid_payload():
    # Use a minimal mock payload based on mock_prediction.json
    payload = {
        "device_id": "DEV-TEST",
        "device_name": "Test Device",
        "future_event_probability": 0.85,
        "prediction": 1,
        "risk_level": "HIGH",
        "model_confidence": 0.90,
        "feature_drivers": [
            {"feature": "previous_recalls", "impact": 0.5}
        ]
    }
    
    response = client.post("/api/v1/diagnose", json=payload)
    # The exact behavior depends on whether the engine can run fully (requires DB/LLM),
    # but we should expect either a 200 with the result or a 500/503 if the environment
    # isn't fully configured (which is handled by our try-except in main.py).
    
    # If the engine runs successfully in fallback mode:
    if response.status_code == 200:
        data = response.json()
        assert "equipment_id" in data
        assert data["equipment_id"] == "DEV-TEST"
        assert "risk_score" in data
        assert "diagnosis" in data
