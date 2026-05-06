from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.schemas.stock import StockHistoryResponse, StockQuoteResponse
from backend.app.services.finnhub_service import FinnhubService, get_finnhub_service

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("/{ticker}/quote", response_model=StockQuoteResponse)
async def read_stock_quote(
    ticker: str,
    finnhub: FinnhubService = Depends(get_finnhub_service),
) -> StockQuoteResponse:
    try:
        data = await finnhub.get_stock_quote(ticker)
        return StockQuoteResponse(**data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@router.get("/{ticker}/history", response_model=StockHistoryResponse)
async def read_stock_history(
    ticker: str,
    finnhub: FinnhubService = Depends(get_finnhub_service),
    resolution: str = Query(
        default="D",
        description="Finnhub candle resolution: 1, 5, 15, 30, 60, D, W, M",
        pattern="^(1|5|15|30|60|D|W|M)$",
    ),
    from_ts: int | None = Query(
        default=None,
        description="Range start (Unix seconds). Omit with to_ts to use `days` window ending at `to_ts` or now.",
    ),
    to_ts: int | None = Query(
        default=None,
        description="Range end (Unix seconds). Defaults to now.",
    ),
    days: int = Query(
        default=30,
        ge=1,
        le=3650,
        description="If from_ts is omitted, load this many days before to_ts.",
    ),
) -> StockHistoryResponse:
    try:
        data = await finnhub.get_stock_history(
            ticker,
            resolution=resolution,
            from_ts=from_ts,
            to_ts=to_ts,
            days=days,
        )
        return StockHistoryResponse(**data)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
