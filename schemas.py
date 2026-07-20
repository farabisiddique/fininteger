"""
Pydantic schemas for FastAPI request/response validation.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


class InstrumentBase(BaseModel):
    id: str
    name: str
    category: str
    price: float
    change: float
    volume: str
    market_cap: str
    icon: str


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentResponse(InstrumentBase):
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ForecastData(BaseModel):
    symbol: str
    current_price: float
    demo_mode: Optional[bool] = False
    forecasts: Dict[str, Any]
    sentiment: str
    avg_confidence: int
    signal_bars: Dict[str, int]
    technical_signals: Dict[str, Any]
    market_data: Dict[str, Any]


class Candle(BaseModel):
    time: Union[int, str]  # epoch seconds (intraday) or "YYYY-MM-DD" (daily)
    open: float
    high: float
    low: float
    close: float
    volume: float


class HistoryData(BaseModel):
    symbol: str
    period: str
    demo_mode: bool = False
    candles: List[Candle]


class InstrumentsListResponse(BaseModel):
    instruments: List[InstrumentResponse]


class PriceResponse(BaseModel):
    symbol: str
    price: float
    change: Optional[float] = None  # 24h % change vs previous close


class CategoryResponse(BaseModel):
    id: str
    label: str


class CategoriesListResponse(BaseModel):
    categories: List[CategoryResponse]
