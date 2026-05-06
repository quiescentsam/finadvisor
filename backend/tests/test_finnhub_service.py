import pytest
import respx
from httpx import Response

from backend.app.services.finnhub_service import FinnhubService


@pytest.fixture
def finnhub_service() -> FinnhubService:
    return FinnhubService(api_key="test-token")


@pytest.mark.asyncio
@respx.mock
async def test_get_stock_quote(finnhub_service: FinnhubService) -> None:
    respx.get("https://finnhub.io/api/v1/quote").mock(
        return_value=Response(
            200,
            json={
                "c": 190.5,
                "h": 192.0,
                "l": 189.0,
                "o": 191.0,
                "pc": 188.0,
                "t": 1710000000,
            },
        )
    )

    result = await finnhub_service.get_stock_quote("aapl")
    assert result["symbol"] == "AAPL"
    assert result["current_price"] == 190.5
    assert result["open"] == 191.0
    assert result["high"] == 192.0
    assert result["low"] == 189.0
    assert result["previous_close"] == 188.0
    assert result["timestamp"] == 1710000000


@pytest.mark.asyncio
@respx.mock
async def test_get_stock_history(finnhub_service: FinnhubService) -> None:
    respx.get("https://finnhub.io/api/v1/stock/candle").mock(
        return_value=Response(
            200,
            json={
                "s": "ok",
                "t": [100, 200],
                "o": [1.0, 2.0],
                "h": [1.5, 2.5],
                "l": [0.9, 1.9],
                "c": [1.2, 2.2],
                "v": [1000.0, 2000.0],
            },
        )
    )

    result = await finnhub_service.get_stock_history(
        "AAPL", resolution="D", from_ts=50, to_ts=300
    )
    assert result["symbol"] == "AAPL"
    assert result["resolution"] == "D"
    assert result["status"] == "ok"
    assert len(result["bars"]) == 2
    assert result["bars"][0]["time"] == 100
    assert result["bars"][0]["close"] == 1.2


@pytest.mark.asyncio
@respx.mock
async def test_get_company_profile(finnhub_service: FinnhubService) -> None:
    respx.get("https://finnhub.io/api/v1/stock/profile2").mock(
        return_value=Response(
            200,
            json={"name": "Apple Inc", "ticker": "AAPL"},
        )
    )

    profile = await finnhub_service.get_company_profile("AAPL")
    assert profile["name"] == "Apple Inc"
    assert profile["ticker"] == "AAPL"
