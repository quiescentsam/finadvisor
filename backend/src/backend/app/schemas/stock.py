from pydantic import BaseModel, Field


class StockPriceResponse(BaseModel):
    ticker: str
    price: float


class StockQuoteResponse(BaseModel):
    symbol: str
    current_price: float
    open: float | None = None
    high: float | None = None
    low: float | None = None
    previous_close: float | None = None
    timestamp: int | None = None


class OhlcvBar(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class StockHistoryResponse(BaseModel):
    symbol: str
    resolution: str
    status: str
    bars: list[OhlcvBar] = Field(default_factory=list)
