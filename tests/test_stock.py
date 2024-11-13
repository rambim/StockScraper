from dataclasses import dataclass
from unittest.mock import patch

from fastapi.testclient import TestClient

from src import app
from src.schemas.stock_schemas import PolygonResponse, StockValues

client = TestClient(app)


def test_purchase_stock():
    response = client.post(
        "/api/v1/stock/TEST",
        json={"amount": 10},
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "10 units of stock TEST were added to your stock record"
    }


def test_get_stocks():
    response = client.get("/api/v1/stock/TEST")
    assert response.status_code == 200
    data = response.json()
    assert data["company_code"] == "TEST"
    assert data["purchased_amount"] == 10


@patch("src.services.stock_service.PolygonAPI.get_stock_values")
@patch("src.services.stock_service.Redis.get")
def test_stock_api_not_found(mock_redis_get, mock_get_stock_values):

    mock_redis_get.return_value = None
    mock_get_stock_values.return_value = PolygonResponse(
        status="error", stock_values=StockValues(open=0.0, high=0.0, low=0.0, close=0.0)
    )

    response = client.get("/api/v1/stock/AAPL")
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert response.json()["stock_values"] == {
        "open": 0.0,
        "high": 0.0,
        "low": 0.0,
        "close": 0.0,
    }
