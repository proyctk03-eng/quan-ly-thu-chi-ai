"""Integration tests for FastAPI REST endpoints."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.database import init_db

@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before running API tests."""
    init_db()

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "FastAPI Backend"}

def test_get_transactions():
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_delete_transaction():
    # 1. Create transaction
    payload = {
        "loai": "Chi",
        "so_tien": 45000.0,
        "danh_muc": "Ăn uống",
        "ngay": "2026-08-12",
        "ghi_chu": "Bún chả trưa"
    }
    create_res = client.post("/api/v1/transactions", json=payload)
    assert create_res.status_code == 200
    data = create_res.json()
    assert "id" in data
    tx_id = data["id"]

    # 2. Delete transaction
    del_res = client.delete(f"/api/v1/transactions/{tx_id}")
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

def test_get_budgets():
    response = client.get("/api/v1/budgets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_set_budget():
    payload = {
        "danh_muc": "Ăn uống",
        "so_tien_limit": 3000000.0
    }
    res = client.post("/api/v1/budgets", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

def test_analytics_summary():
    res = client.get("/api/v1/analytics/summary")
    assert res.status_code == 200
    data = res.json()
    assert "tong_thu" in data
    assert "tong_chi" in data
    assert "so_du" in data

def test_analytics_monthly_comparison():
    res = client.get("/api/v1/analytics/monthly-comparison")
    assert res.status_code == 200
    data = res.json()
    assert "current_month" in data
