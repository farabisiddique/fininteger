"""
Database initialization script.
Populates the database with initial instrument data.
Run once with: python init_db.py
"""

from database import SessionLocal, init_db
from models import Instrument

INSTRUMENTS = [
    {"id": "BTC",    "name": "Bitcoin",          "cat": "crypto",      "price": 67420.50, "change": 2.34,  "vol": "38.2B", "mcap": "1.32T", "icon": "B"},
    {"id": "ETH",    "name": "Ethereum",          "cat": "crypto",      "price": 3842.10,  "change": -1.12, "vol": "18.7B", "mcap": "462B",  "icon": "E"},
    {"id": "SOL",    "name": "Solana",             "cat": "crypto",      "price": 182.45,   "change": 5.67,  "vol": "4.1B",  "mcap": "85B",   "icon": "S"},
    {"id": "AAPL",   "name": "Apple Inc.",         "cat": "stocks",      "price": 228.35,   "change": 1.45,  "vol": "52M",   "mcap": "3.52T", "icon": "A"},
    {"id": "NVDA",   "name": "NVIDIA Corp.",       "cat": "stocks",      "price": 875.20,   "change": 3.21,  "vol": "41M",   "mcap": "2.16T", "icon": "N"},
    {"id": "TSLA",   "name": "Tesla Inc.",         "cat": "stocks",      "price": 242.10,   "change": -2.88, "vol": "95M",   "mcap": "775B",  "icon": "T"},
    {"id": "XAU",    "name": "Gold",               "cat": "commodities", "price": 2312.40,  "change": 0.34,  "vol": "142B",  "mcap": "-",     "icon": "Au"},
    {"id": "OIL",    "name": "Crude Oil",          "cat": "commodities", "price": 78.92,    "change": 1.56,  "vol": "29B",   "mcap": "-",     "icon": "O"},
    {"id": "SPY",    "name": "SPDR S&P 500",       "cat": "etfs",        "price": 542.10,   "change": 0.88,  "vol": "72M",   "mcap": "498B",  "icon": "S"},
    {"id": "EURUSD", "name": "EUR/USD",            "cat": "forex",       "price": 1.0842,   "change": 0.12,  "vol": "6.8T",  "mcap": "-",     "icon": "$"},
]


def seed_instruments(db, force: bool = False) -> int:
    """Insert the instrument seed data. Skips if the table already has rows
    unless force=True (which wipes and re-inserts). Returns rows added."""
    if force:
        db.query(Instrument).delete()
        db.commit()
    elif db.query(Instrument).first() is not None:
        return 0

    for inst in INSTRUMENTS:
        db.add(Instrument(
            id=inst["id"],
            name=inst["name"],
            category=inst["cat"],
            price=inst["price"],
            change=inst["change"],
            volume=inst["vol"],
            market_cap=inst["mcap"],
            icon=inst["icon"]
        ))
    db.commit()
    return len(INSTRUMENTS)


def main():
    print("Initializing database...")
    init_db()
    print("Database tables created.")

    db = SessionLocal()
    print(f"Adding {len(INSTRUMENTS)} instruments...")
    seed_instruments(db, force=True)
    db.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    main()
