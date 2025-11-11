import os
import pytest
from backend.app.services.finnhub_service import FinnhubService

@pytest.fixture(scope="module")
def finnhub_service():
    os.environ["FINNHUB_API_KEY"] = "demo"  # Finnhub provides a public 'demo' key
    return FinnhubService()

def test_get_stock_quote(finnhub_service):
    result = finnhub_service.get_stock_quote("AAPL")
    assert "current_price" in result
    assert result["symbol"] == "AAPL"
    assert isinstance(result["current_price"], (float, int))

def test_get_company_profile(finnhub_service):
    profile = finnhub_service.get_company_profile("AAPL")
    assert "name" in profile
    assert profile["ticker"] == "AAPL"
