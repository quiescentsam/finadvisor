"""HTTP tests for FastAPI routes; service layer is mocked and call paths are asserted."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from starlette.testclient import TestClient

from backend.app.main import app
from backend.app.services.finnhub_service import FinnhubService, get_finnhub_service
from backend.config.settings import settings


def _quote_service_dict() -> dict:
    return {
        "symbol": "AAPL",
        "current_price": 190.5,
        "open": 191.0,
        "high": 192.0,
        "low": 189.0,
        "previous_close": 188.0,
        "timestamp": 1_710_000_000,
    }


def _history_service_dict() -> dict:
    return {
        "symbol": "AAPL",
        "resolution": "D",
        "status": "ok",
        "bars": [
            {
                "time": 1_700_000_000,
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 100.5,
                "volume": 1_000_000.0,
            }
        ],
    }


@pytest.fixture
def mock_finnhub() -> AsyncMock:
    service = AsyncMock(spec=FinnhubService)
    service.get_stock_quote = AsyncMock(return_value=_quote_service_dict())
    service.get_stock_history = AsyncMock(return_value=_history_service_dict())
    return service


@pytest.fixture
def stocks_client(mock_finnhub: AsyncMock):
    app.dependency_overrides[get_finnhub_service] = lambda: mock_finnhub
    with TestClient(app) as client:
        yield client, mock_finnhub
    app.dependency_overrides.pop(get_finnhub_service, None)


def test_get_stock_quote_endpoint_calls_finnhub_and_returns_body(stocks_client):
    client, finnhub = stocks_client

    r = client.get("/api/v1/stocks/aapl/quote")

    assert r.status_code == 200
    body = r.json()
    assert body["symbol"] == "AAPL"
    assert body["current_price"] == 190.5
    assert body["open"] == 191.0
    finnhub.get_stock_quote.assert_awaited_once_with("aapl")


def test_stock_routes_503_when_finnhub_not_configured():
    prev = settings.FINNHUB_API_KEY
    settings.FINNHUB_API_KEY = None
    try:
        with TestClient(app) as client:
            r = client.get("/api/v1/stocks/aapl/quote")
        assert r.status_code == 503
        assert "FINNHUB_API_KEY" in r.json()["detail"]
    finally:
        settings.FINNHUB_API_KEY = prev


def test_get_stock_quote_value_error_maps_to_404(stocks_client):
    client, finnhub = stocks_client
    finnhub.get_stock_quote = AsyncMock(side_effect=ValueError("no quote"))

    r = client.get("/api/v1/stocks/zzz/quote")

    assert r.status_code == 404
    assert "no quote" in r.json()["detail"]
    finnhub.get_stock_quote.assert_awaited_once_with("zzz")


def test_get_stock_quote_runtime_error_maps_to_502(stocks_client):
    client, finnhub = stocks_client
    finnhub.get_stock_quote = AsyncMock(side_effect=RuntimeError("upstream"))

    r = client.get("/api/v1/stocks/aapl/quote")

    assert r.status_code == 502
    assert r.json()["detail"] == "upstream"
    finnhub.get_stock_quote.assert_awaited_once_with("aapl")


def test_get_stock_history_endpoint_calls_finnhub_with_defaults(stocks_client):
    client, finnhub = stocks_client

    r = client.get("/api/v1/stocks/aapl/history")

    assert r.status_code == 200
    body = r.json()
    assert body["symbol"] == "AAPL"
    assert body["resolution"] == "D"
    assert body["status"] == "ok"
    assert len(body["bars"]) == 1
    assert body["bars"][0]["close"] == 100.5
    finnhub.get_stock_history.assert_awaited_once_with(
        "aapl",
        resolution="D",
        from_ts=None,
        to_ts=None,
        days=30,
    )


def test_get_stock_history_endpoint_passes_query_params_to_service(stocks_client):
    client, finnhub = stocks_client

    r = client.get(
        "/api/v1/stocks/msft/history",
        params={"resolution": "W", "days": 90, "from_ts": 100, "to_ts": 200},
    )

    assert r.status_code == 200
    finnhub.get_stock_history.assert_awaited_once_with(
        "msft",
        resolution="W",
        from_ts=100,
        to_ts=200,
        days=90,
    )


def test_get_stock_history_runtime_error_maps_to_502(stocks_client):
    client, finnhub = stocks_client
    finnhub.get_stock_history = AsyncMock(side_effect=RuntimeError("finnhub down"))

    r = client.get("/api/v1/stocks/aapl/history")

    assert r.status_code == 502
    finnhub.get_stock_history.assert_awaited_once_with(
        "aapl",
        resolution="D",
        from_ts=None,
        to_ts=None,
        days=30,
    )


@patch("backend.app.routes.ai.get_recommendation", new_callable=AsyncMock)
def test_ai_recommendation_endpoint_calls_service(mock_get_recommendation: AsyncMock):
    mock_get_recommendation.return_value = {
        "user_id": 7,
        "advice": ["Hold cash"],
    }

    with TestClient(app) as client:
        r = client.post("/api/v1/ai/recommendation", params={"user_id": 7})

    assert r.status_code == 200
    assert r.json() == {"user_id": 7, "advice": ["Hold cash"]}
    mock_get_recommendation.assert_awaited_once_with(7)
