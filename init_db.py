"""
Database initialization script.
Populates the database with initial instrument data.
Run once with: python init_db.py
"""

from database import SessionLocal, init_db
from models import Instrument

INSTRUMENTS = [
    # ── Crypto (12) ────────────────────────────────────────────────────────────
    {"id": "BTC",    "name": "Bitcoin",          "cat": "crypto",      "price": 67420.50, "change": 2.34,  "vol": "38.2B", "mcap": "1.32T", "icon": "₿"},
    {"id": "ETH",    "name": "Ethereum",          "cat": "crypto",      "price": 3842.10,  "change": -1.12, "vol": "18.7B", "mcap": "462B",  "icon": "Ξ"},
    {"id": "SOL",    "name": "Solana",             "cat": "crypto",      "price": 182.45,   "change": 5.67,  "vol": "4.1B",  "mcap": "85B",   "icon": "◎"},
    {"id": "BNB",    "name": "BNB",                "cat": "crypto",      "price": 598.30,   "change": 0.88,  "vol": "1.9B",  "mcap": "92B",   "icon": "B"},
    {"id": "XRP",    "name": "Ripple",             "cat": "crypto",      "price": 0.6210,   "change": -0.43, "vol": "1.2B",  "mcap": "34B",   "icon": "✕"},
    {"id": "ADA",    "name": "Cardano",            "cat": "crypto",      "price": 0.4520,   "change": 1.85,  "vol": "420M",  "mcap": "16B",   "icon": "₳"},
    {"id": "DOGE",   "name": "Dogecoin",           "cat": "crypto",      "price": 0.1385,   "change": 7.42,  "vol": "1.1B",  "mcap": "20B",   "icon": "Ð"},
    {"id": "DOT",    "name": "Polkadot",           "cat": "crypto",      "price": 6.84,     "change": -2.15, "vol": "180M",  "mcap": "9.8B",  "icon": "●"},
    {"id": "AVAX",   "name": "Avalanche",          "cat": "crypto",      "price": 28.90,    "change": 3.44,  "vol": "310M",  "mcap": "11B",   "icon": "▲"},
    {"id": "LINK",   "name": "Chainlink",          "cat": "crypto",      "price": 14.25,    "change": 2.05,  "vol": "390M",  "mcap": "8.4B",  "icon": "⬡"},
    {"id": "LTC",    "name": "Litecoin",           "cat": "crypto",      "price": 84.15,    "change": -0.95, "vol": "350M",  "mcap": "6.3B",  "icon": "Ł"},
    {"id": "TRX",    "name": "TRON",               "cat": "crypto",      "price": 0.1240,   "change": 0.65,  "vol": "320M",  "mcap": "10.8B", "icon": "♦"},
    # ── Stocks (12) ────────────────────────────────────────────────────────────
    {"id": "AAPL",   "name": "Apple Inc.",         "cat": "stocks",      "price": 228.35,   "change": 1.45,  "vol": "52M",   "mcap": "3.52T", "icon": "A"},
    {"id": "NVDA",   "name": "NVIDIA Corp.",       "cat": "stocks",      "price": 875.20,   "change": 3.21,  "vol": "41M",   "mcap": "2.16T", "icon": "N"},
    {"id": "MSFT",   "name": "Microsoft",          "cat": "stocks",      "price": 418.90,   "change": 0.67,  "vol": "22M",   "mcap": "3.11T", "icon": "M"},
    {"id": "TSLA",   "name": "Tesla Inc.",         "cat": "stocks",      "price": 242.10,   "change": -2.88, "vol": "95M",   "mcap": "775B",  "icon": "T"},
    {"id": "AMZN",   "name": "Amazon.com",         "cat": "stocks",      "price": 196.45,   "change": 1.12,  "vol": "38M",   "mcap": "2.07T", "icon": "A"},
    {"id": "GOOGL",  "name": "Alphabet Inc.",      "cat": "stocks",      "price": 178.35,   "change": 0.92,  "vol": "25M",   "mcap": "2.21T", "icon": "G"},
    {"id": "META",   "name": "Meta Platforms",     "cat": "stocks",      "price": 512.20,   "change": 1.78,  "vol": "18M",   "mcap": "1.30T", "icon": "M"},
    {"id": "NFLX",   "name": "Netflix Inc.",       "cat": "stocks",      "price": 645.80,   "change": -1.35, "vol": "4.2M",  "mcap": "278B",  "icon": "N"},
    {"id": "AMD",    "name": "Adv. Micro Devices", "cat": "stocks",      "price": 162.45,   "change": 4.12,  "vol": "62M",   "mcap": "262B",  "icon": "A"},
    {"id": "INTC",   "name": "Intel Corp.",        "cat": "stocks",      "price": 30.85,    "change": -3.65, "vol": "48M",   "mcap": "131B",  "icon": "I"},
    {"id": "JPM",    "name": "JPMorgan Chase",     "cat": "stocks",      "price": 198.50,   "change": 0.45,  "vol": "9.8M",  "mcap": "571B",  "icon": "J"},
    {"id": "V",      "name": "Visa Inc.",          "cat": "stocks",      "price": 275.60,   "change": 0.28,  "vol": "6.1M",  "mcap": "562B",  "icon": "V"},
    # ── Commodities (14) ───────────────────────────────────────────────────────
    {"id": "XAU",    "name": "Gold",               "cat": "commodities", "price": 2312.40,  "change": 0.34,  "vol": "142B",  "mcap": "—",     "icon": "Au"},
    {"id": "XAG",    "name": "Silver",             "cat": "commodities", "price": 27.84,    "change": -0.21, "vol": "9.4B",  "mcap": "—",     "icon": "Ag"},
    {"id": "OIL",    "name": "Crude Oil",          "cat": "commodities", "price": 78.92,    "change": 1.56,  "vol": "29B",   "mcap": "—",     "icon": "🛢"},
    {"id": "NG",     "name": "Natural Gas",        "cat": "commodities", "price": 2.145,    "change": -3.22, "vol": "8.1B",  "mcap": "—",     "icon": "⛽"},
    {"id": "HG",     "name": "Copper",             "cat": "commodities", "price": 4.485,    "change": 1.12,  "vol": "6.2B",  "mcap": "—",     "icon": "Cu"},
    {"id": "PL",     "name": "Platinum",           "cat": "commodities", "price": 968.40,   "change": -0.85, "vol": "1.1B",  "mcap": "—",     "icon": "Pt"},
    {"id": "PA",     "name": "Palladium",          "cat": "commodities", "price": 942.60,   "change": -1.92, "vol": "720M",  "mcap": "—",     "icon": "Pd"},
    {"id": "ZC",     "name": "Corn",               "cat": "commodities", "price": 452.25,   "change": 0.64,  "vol": "2.4B",  "mcap": "—",     "icon": "🌽"},
    {"id": "ZW",     "name": "Wheat",              "cat": "commodities", "price": 568.50,   "change": -1.28, "vol": "1.9B",  "mcap": "—",     "icon": "🌾"},
    {"id": "ZS",     "name": "Soybeans",           "cat": "commodities", "price": 1182.75,  "change": 0.35,  "vol": "2.1B",  "mcap": "—",     "icon": "So"},
    {"id": "KC",     "name": "Coffee",             "cat": "commodities", "price": 228.85,   "change": 2.31,  "vol": "890M",  "mcap": "—",     "icon": "☕"},
    {"id": "SB",     "name": "Sugar",              "cat": "commodities", "price": 19.42,    "change": -0.55, "vol": "640M",  "mcap": "—",     "icon": "Su"},
    {"id": "CT",     "name": "Cotton",             "cat": "commodities", "price": 71.28,    "change": 0.88,  "vol": "410M",  "mcap": "—",     "icon": "Ct"},
    {"id": "CC",     "name": "Cocoa",              "cat": "commodities", "price": 7845.00,  "change": 5.85,  "vol": "520M",  "mcap": "—",     "icon": "Cc"},
    # ── ETFs (10) ──────────────────────────────────────────────────────────────
    {"id": "SPY",    "name": "SPDR S&P 500",       "cat": "etfs",        "price": 542.10,   "change": 0.88,  "vol": "72M",   "mcap": "498B",  "icon": "S"},
    {"id": "QQQ",    "name": "Invesco QQQ",        "cat": "etfs",        "price": 468.35,   "change": 1.22,  "vol": "45M",   "mcap": "241B",  "icon": "Q"},
    {"id": "VTI",    "name": "Vanguard Total",     "cat": "etfs",        "price": 248.90,   "change": 0.55,  "vol": "3.2M",  "mcap": "398B",  "icon": "V"},
    {"id": "IWM",    "name": "iShares Russell 2K", "cat": "etfs",        "price": 201.35,   "change": 1.15,  "vol": "32M",   "mcap": "66B",   "icon": "I"},
    {"id": "DIA",    "name": "SPDR Dow Jones",     "cat": "etfs",        "price": 392.80,   "change": 0.42,  "vol": "3.4M",  "mcap": "33B",   "icon": "D"},
    {"id": "EFA",    "name": "iShares MSCI EAFE",  "cat": "etfs",        "price": 78.95,    "change": 0.35,  "vol": "16M",   "mcap": "55B",   "icon": "E"},
    {"id": "GLD",    "name": "SPDR Gold Shares",   "cat": "etfs",        "price": 214.50,   "change": 0.30,  "vol": "6.8M",  "mcap": "62B",   "icon": "G"},
    {"id": "XLK",    "name": "Technology Select",  "cat": "etfs",        "price": 228.70,   "change": 1.35,  "vol": "5.9M",  "mcap": "71B",   "icon": "X"},
    {"id": "XLF",    "name": "Financial Select",   "cat": "etfs",        "price": 41.85,    "change": -0.52, "vol": "34M",   "mcap": "39B",   "icon": "X"},
    {"id": "ARKK",   "name": "ARK Innovation",     "cat": "etfs",        "price": 44.62,    "change": -2.24, "vol": "12M",   "mcap": "6.7B",  "icon": "A"},
    # ── Forex (10) ─────────────────────────────────────────────────────────────
    {"id": "EURUSD", "name": "EUR/USD",            "cat": "forex",       "price": 1.0842,   "change": 0.12,  "vol": "6.8T",  "mcap": "—",     "icon": "€"},
    {"id": "GBPUSD", "name": "GBP/USD",            "cat": "forex",       "price": 1.2710,   "change": -0.08, "vol": "3.1T",  "mcap": "—",     "icon": "£"},
    {"id": "USDJPY", "name": "USD/JPY",            "cat": "forex",       "price": 151.84,   "change": 0.33,  "vol": "4.4T",  "mcap": "—",     "icon": "¥"},
    {"id": "AUDUSD", "name": "AUD/USD",            "cat": "forex",       "price": 0.6648,   "change": 0.22,  "vol": "1.4T",  "mcap": "—",     "icon": "A$"},
    {"id": "USDCAD", "name": "USD/CAD",            "cat": "forex",       "price": 1.3712,   "change": -0.15, "vol": "1.2T",  "mcap": "—",     "icon": "C$"},
    {"id": "USDCHF", "name": "USD/CHF",            "cat": "forex",       "price": 0.8985,   "change": 0.08,  "vol": "990B",  "mcap": "—",     "icon": "₣"},
    {"id": "NZDUSD", "name": "NZD/USD",            "cat": "forex",       "price": 0.6112,   "change": 0.31,  "vol": "580B",  "mcap": "—",     "icon": "N$"},
    {"id": "EURGBP", "name": "EUR/GBP",            "cat": "forex",       "price": 0.8530,   "change": 0.05,  "vol": "810B",  "mcap": "—",     "icon": "€£"},
    {"id": "EURJPY", "name": "EUR/JPY",            "cat": "forex",       "price": 164.62,   "change": 0.44,  "vol": "720B",  "mcap": "—",     "icon": "€¥"},
    {"id": "GBPJPY", "name": "GBP/JPY",            "cat": "forex",       "price": 193.05,   "change": -0.26, "vol": "610B",  "mcap": "—",     "icon": "£¥"},
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
