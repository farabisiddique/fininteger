"""
Page routes for serving HTML templates via Jinja2.
Instrument data comes from the SQLite `instruments` table (seeded by init_db.py).
"""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from config import SHOW_TOUR_TO_ALL
from database import get_db
from models import Instrument

router = APIRouter(tags=["pages"])

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "forecaster" / "templates" / "forecaster"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

CATEGORIES = [
    {"id": "all",         "label": "ALL"},
    {"id": "crypto",      "label": "CRYPTO"},
    {"id": "stocks",      "label": "STOCKS"},
    {"id": "commodities", "label": "COMMODITIES"},
    {"id": "etfs",        "label": "ETFS"},
    {"id": "forex",       "label": "FOREX"},
]


def get_instruments(db: Session) -> list[dict]:
    """Load instruments from SQLite, shaped the way the frontend JS expects
    (short keys: cat / vol / mcap, matching the original INSTRUMENTS constant)."""
    rows = db.query(Instrument).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "cat": r.category,
            "price": r.price,
            "change": r.change,
            "vol": r.volume,
            "mcap": r.market_cap,
            "icon": r.icon,
        }
        for r in rows
    ]


def render(request: Request, db: Session, template_name: str):
    instruments = get_instruments(db)
    context = {
        "instruments": instruments,
        "instruments_json": json.dumps(instruments),
        "categories": CATEGORIES,
        "show_tour_to_all": SHOW_TOUR_TO_ALL,
    }
    return templates.TemplateResponse(request, template_name, context)


@router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    """Homepage - markets overview."""
    return render(request, db, "index.html")


@router.get("/tools")
async def tools(request: Request, db: Session = Depends(get_db)):
    """Tools page."""
    return render(request, db, "tools.html")


@router.get("/markets")
async def markets(request: Request, db: Session = Depends(get_db)):
    """Markets page."""
    return render(request, db, "markets.html")


@router.get("/portfolio")
async def portfolio(request: Request, db: Session = Depends(get_db)):
    """Portfolio page."""
    return render(request, db, "portfolio.html")


@router.get("/learn")
async def learn(request: Request, db: Session = Depends(get_db)):
    """Learn page — investing / finance / crypto education."""
    return render(request, db, "learn.html")


@router.get("/about")
async def about(request: Request, db: Session = Depends(get_db)):
    """About page."""
    return render(request, db, "about.html")


@router.get("/contact")
async def contact(request: Request, db: Session = Depends(get_db)):
    """Contact page."""
    return render(request, db, "contact.html")
