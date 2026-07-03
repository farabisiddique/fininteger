"""
SQLAlchemy models for SQLite database.
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from database import Base


class Instrument(Base):
    """Instrument metadata (crypto, stocks, commodities, ETFs, forex)"""
    __tablename__ = "instruments"

    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # crypto, stocks, commodities, etfs, forex
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=False)  # Percentage change
    volume = Column(String(50), nullable=False)
    market_cap = Column(String(50), nullable=False)
    icon = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ForecastCache(Base):
    """Cache for forecast results with TTL"""
    __tablename__ = "forecast_cache"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, unique=True, index=True)
    forecast_data = Column(JSON, nullable=False)  # Stores the full forecast JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)  # TTL expiration time

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return datetime.utcnow() > self.expires_at
