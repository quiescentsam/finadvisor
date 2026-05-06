"""Finnhub REST client (quote + candle history)."""

from __future__ import annotations

import time
from typing import Any

import httpx

from backend.config.settings import settings

FINNHUB_BASE = "https://finnhub.io/api/v1"


class FinnhubService:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.FINNHUB_API_KEY
        if not self.api_key:
            raise ValueError("Missing FINNHUB_API_KEY environment variable")

    async def get_stock_quote(self, symbol: str) -> dict[str, Any]:
        sym = symbol.upper().strip()
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(
                f"{FINNHUB_BASE}/quote",
                params={"symbol": sym, "token": self.api_key},
            )
        if r.status_code != 200:
            raise RuntimeError(f"Finnhub API error: {r.status_code} - {r.text}")

        data = r.json()
        if not data or data.get("c") in (0, None):
            raise ValueError(f"Finnhub returned no valid quote data for {sym}: {data}")

        return {
            "symbol": sym,
            "current_price": float(data["c"]),
            "open": _f(data.get("o")),
            "high": _f(data.get("h")),
            "low": _f(data.get("l")),
            "previous_close": _f(data.get("pc")),
            "timestamp": data.get("t"),
        }

    async def get_stock_history(
        self,
        symbol: str,
        *,
        resolution: str = "D",
        from_ts: int | None = None,
        to_ts: int | None = None,
        days: int = 30,
    ) -> dict[str, Any]:
        sym = symbol.upper().strip()
        now = int(time.time())
        to_t = to_ts if to_ts is not None else now
        from_t = from_ts if from_ts is not None else to_t - max(1, days) * 86400

        params = {
            "symbol": sym,
            "resolution": resolution,
            "from": from_t,
            "to": to_t,
            "token": self.api_key,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.get(f"{FINNHUB_BASE}/stock/candle", params=params)
        if r.status_code != 200:
            raise RuntimeError(f"Finnhub API error: {r.status_code} - {r.text}")

        data = r.json()
        status = data.get("s", "unknown")
        if status != "ok":
            return {"symbol": sym, "resolution": resolution, "status": status, "bars": []}

        times = data.get("t") or []
        opens = data.get("o") or []
        highs = data.get("h") or []
        lows = data.get("l") or []
        closes = data.get("c") or []
        volumes = data.get("v") or []

        bars: list[dict[str, Any]] = []
        for i, t in enumerate(times):
            bars.append(
                {
                    "time": int(t),
                    "open": float(opens[i]) if i < len(opens) else 0.0,
                    "high": float(highs[i]) if i < len(highs) else 0.0,
                    "low": float(lows[i]) if i < len(lows) else 0.0,
                    "close": float(closes[i]) if i < len(closes) else 0.0,
                    "volume": float(volumes[i]) if i < len(volumes) else 0.0,
                }
            )

        return {"symbol": sym, "resolution": resolution, "status": status, "bars": bars}

    async def get_company_profile(self, symbol: str) -> dict[str, Any]:
        sym = symbol.upper().strip()
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(
                f"{FINNHUB_BASE}/stock/profile2",
                params={"symbol": sym, "token": self.api_key},
            )
        if r.status_code != 200:
            raise RuntimeError(f"Finnhub API error: {r.status_code} - {r.text}")
        return r.json()


def _f(v: Any) -> float | None:
    if v is None:
        return None
    return float(v)


def get_finnhub_service() -> FinnhubService:
    return FinnhubService()
