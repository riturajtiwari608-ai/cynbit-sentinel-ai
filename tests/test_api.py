"""
Integration tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["service"] == "Cynbit AI Sentinel"


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_analyze_endpoint():
    payload = {
        "text": "The food was delicious and the rooftop ambiance was wonderful.",
        "business_name": "Test Bistro",
        "branch_location": "Jaipur",
        "rating": 5,
        "customer_tier": "VIP"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["sentiment_intelligence"]["overall_sentiment"] == "Positive"


def test_crisis_scan_endpoint():
    payload = {"text": "We are reporting this to the police and filing with consumer court for fraud."}
    response = client.post("/api/v1/crisis-scan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["has_crisis_trigger"] is True
    assert "LEGAL_REGULATORY" in data["matched_categories"]
