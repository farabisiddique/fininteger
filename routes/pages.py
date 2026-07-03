"""
Page routes for serving HTML templates.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

router = APIRouter(tags=["pages"])

# Initialize instrument data for templates
INSTRUMENTS = [
    {"id": "BTC",    "name": "Bitcoin",        "cat": "crypto",      "price": 67420.50, "change": 2.34,  "vol": "38.2B", "mcap": "1.32T", "icon": "₿"},
    {"id": "ETH",    "name": "Ethereum",        "cat": "crypto",      "price": 3842.10,  "change": -1.12, "vol": "18.7B", "mcap": "462B",  "icon": "Ξ"},
    {"id": "SOL",    "name": "Solana",           "cat": "crypto",      "price": 182.45,   "change": 5.67,  "vol": "4.1B",  "mcap": "85B",   "icon": "◎"},
    {"id": "BNB",    "name": "BNB",              "cat": "crypto",      "price": 598.30,   "change": 0.88,  "vol": "1.9B",  "mcap": "92B",   "icon": "B"},
    {"id": "XRP",    "name": "Ripple",           "cat": "crypto",      "price": 0.6210,   "change": -0.43, "vol": "1.2B",  "mcap": "34B",   "icon": "✕"},
    {"id": "AAPL",   "name": "Apple Inc.",       "cat": "stocks",      "price": 228.35,   "change": 1.45,  "vol": "52M",   "mcap": "3.52T", "icon": "A"},
    {"id": "NVDA",   "name": "NVIDIA Corp.",     "cat": "stocks",      "price": 875.20,   "change": 3.21,  "vol": "41M",   "mcap": "2.16T", "icon": "N"},
    {"id": "MSFT",   "name": "Microsoft",        "cat": "stocks",      "price": 418.90,   "change": 0.67,  "vol": "22M",   "mcap": "3.11T", "icon": "M"},
    {"id": "TSLA",   "name": "Tesla Inc.",       "cat": "stocks",      "price": 242.10,   "change": -2.88, "vol": "95M",   "mcap": "775B",  "icon": "T"},
    {"id": "AMZN",   "name": "Amazon.com",       "cat": "stocks",      "price": 196.45,   "change": 1.12,  "vol": "38M",   "mcap": "2.07T", "icon": "A"},
    {"id": "XAU",    "name": "Gold",             "cat": "commodities", "price": 2312.40,  "change": 0.34,  "vol": "142B",  "mcap": "—",     "icon": "Au"},
    {"id": "XAG",    "name": "Silver",           "cat": "commodities", "price": 27.84,    "change": -0.21, "vol": "9.4B",  "mcap": "—",     "icon": "Ag"},
    {"id": "OIL",    "name": "Crude Oil",        "cat": "commodities", "price": 78.92,    "change": 1.56,  "vol": "29B",   "mcap": "—",     "icon": "🛢"},
    {"id": "NG",     "name": "Natural Gas",      "cat": "commodities", "price": 2.145,    "change": -3.22, "vol": "8.1B",  "mcap": "—",     "icon": "⛽"},
    {"id": "SPY",    "name": "SPDR S&P 500",     "cat": "etfs",        "price": 542.10,   "change": 0.88,  "vol": "72M",   "mcap": "498B",  "icon": "S"},
    {"id": "QQQ",    "name": "Invesco QQQ",      "cat": "etfs",        "price": 468.35,   "change": 1.22,  "vol": "45M",   "mcap": "241B",  "icon": "Q"},
    {"id": "VTI",    "name": "Vanguard Total",   "cat": "etfs",        "price": 248.90,   "change": 0.55,  "vol": "3.2M",  "mcap": "398B",  "icon": "V"},
    {"id": "EURUSD", "name": "EUR/USD",          "cat": "forex",       "price": 1.0842,   "change": 0.12,  "vol": "6.8T",  "mcap": "—",     "icon": "€"},
    {"id": "GBPUSD", "name": "GBP/USD",          "cat": "forex",       "price": 1.2710,   "change": -0.08, "vol": "3.1T",  "mcap": "—",     "icon": "£"},
    {"id": "USDJPY", "name": "USD/JPY",          "cat": "forex",       "price": 151.84,   "change": 0.33,  "vol": "4.4T",  "mcap": "—",     "icon": "¥"},
]

CATEGORIES = [
    {"id": "all",         "label": "ALL"},
    {"id": "crypto",      "label": "CRYPTO"},
    {"id": "stocks",      "label": "STOCKS"},
    {"id": "commodities", "label": "COMMODITIES"},
    {"id": "etfs",        "label": "ETFS"},
    {"id": "forex",       "label": "FOREX"},
]


def get_template_content(template_name: str) -> str:
    """Read template file content."""
    template_path = Path(__file__).parent.parent / "forecaster" / "templates" / "forecaster" / f"{template_name}.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_name}")
    return template_path.read_text()


@router.get("/", response_class=HTMLResponse)
async def index():
    """Homepage - markets overview."""
    content = get_template_content("index")
    instruments_json = json.dumps(INSTRUMENTS)
    content = content.replace("{{ instruments_json }}", instruments_json)
    content = content.replace("{{ instruments_json|safe }}", instruments_json)
    return content


@router.get("/tools", response_class=HTMLResponse)
async def tools():
    """Tools page."""
    content = get_template_content("tools")
    instruments_json = json.dumps(INSTRUMENTS)
    content = content.replace("{{ instruments_json }}", instruments_json)
    content = content.replace("{{ instruments_json|safe }}", instruments_json)
    return content


@router.get("/markets", response_class=HTMLResponse)
async def markets():
    """Markets page."""
    content = get_template_content("markets")
    instruments_json = json.dumps(INSTRUMENTS)
    content = content.replace("{{ instruments_json }}", instruments_json)
    content = content.replace("{{ instruments_json|safe }}", instruments_json)
    return content


@router.get("/portfolio", response_class=HTMLResponse)
async def portfolio():
    """Portfolio page."""
    content = get_template_content("portfolio")
    instruments_json = json.dumps(INSTRUMENTS)
    content = content.replace("{{ instruments_json }}", instruments_json)
    content = content.replace("{{ instruments_json|safe }}", instruments_json)
    return content


@router.get("/about", response_class=HTMLResponse)
async def about():
    """About page."""
    return get_template_content("about")


@router.get("/contact", response_class=HTMLResponse)
async def contact():
    """Contact page."""
    return get_template_content("contact")
