"""
Pydantic schemas for FastAPI request/response validation.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
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


class InstrumentsListResponse(BaseModel):
    instruments: List[InstrumentResponse]


class PriceResponse(BaseModel):
    symbol: str
    price: float


class CategoryResponse(BaseModel):
    id: str
    label: str


class CategoriesListResponse(BaseModel):
    categories: List[CategoryResponse]
