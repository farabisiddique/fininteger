# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

fininteger — a FastAPI web app that forecasts financial instrument prices (crypto, stocks, commodities, ETFs, forex) using XGBoost models trained on-the-fly from yfinance data. Single module is `forecaster`.

## Commands

```powershell
# Install dependencies (Pipfile targets Python 3.13)
pip install -r requirements.txt
# or: pipenv install

# Run dev server
python manage.py runserver

# Run tests
python manage.py test forecaster
```

**Required setup:** `config.py` loads config via `python-dotenv` from `.env` in the project root. `SECRET_KEY` has a default but should be changed in production. Optional: `DEBUG` (defaults False), `ALLOWED_HOSTS` (defaults `['*']`).

## Architecture

**SQLite Database.** The app uses SQLAlchemy ORM with SQLite. Instrument metadata lives in the `Instrument` table in `models.py`, and symbol→yfinance-ticker mapping lives in `SYMBOL_MAP` in [forecaster/ml_engine.py](forecaster/ml_engine.py). **Adding/removing an instrument requires updating both**, plus the `BASE_PRICES` dict in `_demo_forecast` for offline fallback.

**Request flow for forecasts:**
1. `GET /api/forecast/<symbol>/` → `views.api_forecast` checks the local-memory cache (`forecast_<SYMBOL>`, 600s TTL).
2. On miss, `ml_engine.forecast_with_fallback` runs the real pipeline: fetch 2y of daily OHLCV from yfinance → engineer ~40 technical-indicator features (`_add_features`) → train one XGBRegressor per horizon (1d/1w/1m, predicting forward log return) → build the response dict with forecasts, sentiment, signal bars, technical signals, and market data.
3. If yfinance fails (no network / rate limit), it silently falls back to `_demo_forecast`, which generates deterministic pseudo-random data (seeded by symbol + 10-minute window) with the **same response shape** plus `"demo_mode": true`. Any change to the real forecast's response structure must be mirrored in `_demo_forecast` or the UI breaks in offline mode.

Models are trained per-request (nothing is persisted to disk); the 600s cache is the only thing keeping this responsive, so keep caching intact when touching `api_forecast`.

**Other endpoints:** `/api/instruments/` (static list), `/api/price/<symbol>/` (live spot price via `yf.Ticker(...).fast_info`). Page routes (`/`, `/tools/`, `/markets/`, `/about/`, `/contact/`, `/portfolio/`) are all defined in [forecaster/urls.py](forecaster/urls.py).

**Frontend:** each template in `forecaster/templates/forecaster/` is a fully self-contained page — Tailwind via CDN with an inline `tailwind.config` (shared color palette: `bg`, `surface`, `accent`, `gain`, `loss`, etc.), inline CSS, and inline vanilla JS that consumes the JSON APIs. There is no static files directory, no base template, and no build step; shared styling changes must be replicated across templates.

## Gotchas

- `requirements.txt` is UTF-16 encoded — if you rewrite it, keep tooling compatibility in mind (pip reads it fine).
- `ml_engine.py` flattens yfinance's MultiIndex columns in `_fetch_ohlcv`; yfinance API changes tend to break there first.
- Confidence values are heuristics derived from validation MAPE (clamped 40–95), not calibrated probabilities.
