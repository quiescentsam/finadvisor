import pytest
import respx
from httpx import Response
from backend.app.services.yahoo_finance import get_stock_price

@pytest.mark.asyncio
@respx.mock
async def test_get_stock_price():
    ticker = "AAPL"
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"

    # Mock the Yahoo Finance API response
    respx.get(url).mock(
        return_value=Response(
            200,
            json={
                "quoteResponse": {
                    "result": [{"regularMarketPrice": 150.25}],
                    "error": None
                }
            }
        )
    )

    price = await get_stock_price(ticker)
    assert price == 150.25
