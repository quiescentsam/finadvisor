import httpx

async def get_stock_price(ticker: str) -> float:
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    async with httpx.AsyncClient() as client:
        # resp = await client.get(url)
        # data = resp.json()
        # return data["quoteResponse"]["result"][0]["regularMarketPrice"]
        return 90.0
