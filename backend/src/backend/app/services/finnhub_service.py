# src/backend/app/services/finnhub_service.py

import os
import requests
import finnhub
from typing import Dict, Any
from backend.config.settings import settings

FINNHUB_URL = "https://finnhub.io/api/v1/quote" 

class FinnhubService:
    def __init__(self):
        api_key = settings.FINNHUB_API_KEY
        print(api_key)
        if not api_key:
            raise ValueError("Missing FINNHUB_API_KEY environment variable")

        self.client = finnhub.Client(api_key=api_key)

    # def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
    #     """
    #     Get real-time quote data for a symbol.
    #     Returns: dict with open, high, low, current price, etc.
    #     """
    #     data = self.client.quote(symbol)
    #     if not data or "c" not in data:
    #         raise ValueError(f"Invalid response for {symbol}: {data}")
        
        
    #     print(f"Finnhub quote data for {symbol}: {data}")
        
    #     return {
    #         "symbol": symbol,
    #         "current_price": data["c"],
    #         "open": data["o"],
    #         "high": data["h"],
    #         "low": data["l"],
    #         "previous_close": data["pc"],
    #         "timestamp": data["t"],
    #     }


    def get_stock_quote(self, symbol: str):
        params = {"symbol": symbol, "token": settings.FINNHUB_API_KEY}
        response = requests.get(FINNHUB_URL, params=params)

        if response.status_code != 200:
            raise RuntimeError(f"Finnhub API error: {response.status_code} - {response.text}")

        data = response.json()

        if not data or data.get("c", 0) == 0:
            raise ValueError(f"Finnhub returned no valid data for {symbol}: {data}")

        return data

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company fundamentals like name, industry, etc.
        """
        return self.client.company_profile2(symbol=symbol)


# curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=d49k1u1r01qlaebhnp4gd49k1u1r01qlaebhnp50"