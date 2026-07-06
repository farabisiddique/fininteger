"""
API routes for forecast, instruments, and price endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Instrument, ForecastCache
from schemas import InstrumentsListResponse, PriceResponse, ForecastData
from forecaster.ml_engine import forecast_with_fallback as forecast, SYMBOL_MAP
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


@router.get("/instruments", response_model=InstrumentsListResponse)
async def api_instruments(db: Session = Depends(get_db)):
    """Get list of all instruments."""
    instruments = db.query(Instrument).all()
    if not instruments:
        # Return empty if no instruments in DB
        return InstrumentsListResponse(instruments=[])
    return InstrumentsListResponse(instruments=instruments)


@router.get("/price/{symbol}", response_model=PriceResponse)
def api_price(symbol: str):
    """Get current price for a symbol from yfinance (sync def → threadpool)."""
    symbol = symbol.upper()
    
    if symbol not in SYMBOL_MAP:
        raise HTTPException(status_code=404, detail="Unknown symbol")
    
    try:
        ticker = yf.Ticker(SYMBOL_MAP[symbol])
        info = ticker.fast_info
        price = info.last_price
        return PriceResponse(symbol=symbol, price=round(price, 6))
    except Exception as e:
        logger.exception(f"Price fetch failed for {symbol}")
        raise HTTPException(status_code=500, detail=str(e))
