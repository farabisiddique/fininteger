"""
API routes for forecast, instruments, and price endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Instrument, ForecastCache
from schemas import InstrumentsListResponse, PriceResponse, ForecastData, HistoryData
from forecaster.ml_engine import (
    forecast_with_fallback as forecast,
    history_with_fallback,
    live_quote,
    HISTORY_PERIODS,
    SYMBOL_MAP,
)
import yfinance as yf
import json

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["api"])

FORECAST_CACHE_TTL = 600  # 600 seconds


@router.get("/forecast/{symbol}", response_model=ForecastData)
def api_forecast(symbol: str, db: Session = Depends(get_db)):
    """Get forecast for a symbol with 600s cache.

    Sync `def` on purpose: model training takes seconds, so FastAPI must run
    it in the threadpool instead of blocking the event loop.
    """
    symbol = symbol.upper()

    if symbol not in SYMBOL_MAP:
        raise HTTPException(status_code=404, detail=f"Unknown symbol: {symbol}")

    # Check cache (row is unique per symbol; may exist but be expired)
    row = db.query(ForecastCache).filter(ForecastCache.symbol == symbol).first()
    if row and row.expires_at > datetime.utcnow():
        return ForecastData(**row.forecast_data)

    # Fetch fresh forecast
    try:
        result = forecast(symbol)
    except Exception as e:
        logger.exception(f"Forecast failed for {symbol}")
        raise HTTPException(status_code=500, detail=str(e))

    # Upsert the single cache row for this symbol; merge() can't be used here
    # because the autoincrement id would always INSERT and hit UNIQUE(symbol)
    expires_at = datetime.utcnow() + timedelta(seconds=FORECAST_CACHE_TTL)
    if row:
        row.forecast_data = result
        row.expires_at = expires_at
    else:
        db.add(ForecastCache(symbol=symbol, forecast_data=result, expires_at=expires_at))
    db.commit()

    return ForecastData(**result)


# In-memory history cache: (symbol, period) -> (expires_at, payload).
# Per-process (not shared across uvicorn workers) — fine for chart data.
_history_cache: dict = {}
HISTORY_CACHE_TTL = 600


@router.get("/history/{symbol}", response_model=HistoryData)
def api_history(symbol: str, range: str = "1mo"):
    """Daily OHLCV history for the dashboard charts (sync def → threadpool)."""
    symbol = symbol.upper()

    if symbol not in SYMBOL_MAP:
        raise HTTPException(status_code=404, detail=f"Unknown symbol: {symbol}")
    if range not in HISTORY_PERIODS:
        raise HTTPException(status_code=400, detail=f"range must be one of {sorted(HISTORY_PERIODS)}")

    key = (symbol, range)
    hit = _history_cache.get(key)
    if hit and hit[0] > datetime.utcnow():
        return hit[1]

    result = history_with_fallback(symbol, range)
    _history_cache[key] = (datetime.utcnow() + timedelta(seconds=HISTORY_CACHE_TTL), result)
    return result


@router.get("/instruments", response_model=InstrumentsListResponse)
async def api_instruments(db: Session = Depends(get_db)):
    """Get list of all instruments."""
    instruments = db.query(Instrument).all()
    if not instruments:
        # Return empty if no instruments in DB
        return InstrumentsListResponse(instruments=[])
    return InstrumentsListResponse(instruments=instruments)


# Short in-memory price cache so frequent frontend polling never hammers Yahoo.
_price_cache: dict = {}
PRICE_CACHE_TTL = 60


@router.get("/price/{symbol}", response_model=PriceResponse)
def api_price(symbol: str):
    """Current price + 24h change, cached 60s (sync def → threadpool)."""
    symbol = symbol.upper()

    if symbol not in SYMBOL_MAP:
        raise HTTPException(status_code=404, detail="Unknown symbol")

    hit = _price_cache.get(symbol)
    if hit and hit[0] > datetime.utcnow():
        return hit[1]

    try:
        result = live_quote(symbol)
    except Exception as e:
        logger.exception(f"Price fetch failed for {symbol}")
        raise HTTPException(status_code=500, detail=str(e))

    _price_cache[symbol] = (datetime.utcnow() + timedelta(seconds=PRICE_CACHE_TTL), result)
    return result
