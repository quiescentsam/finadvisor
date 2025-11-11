from fastapi import APIRouter
from backend.app.services.yahoo_finance import get_stock_price
from backend.app.schemas.stock import StockPriceResponse

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/{ticker}", response_model=StockPriceResponse)
async def read_stock_price(ticker: str):
    price = await get_stock_price(ticker)
    return {"ticker": ticker, "price": price}
