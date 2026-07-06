# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

fininteger — a FastAPI web app that forecasts financial instrument prices (crypto, stocks, commodities, ETFs, forex) using XGBoost models trained on-the-fly from yfinance data. Converted from Django; SQLite (via SQLAlchemy 2.0) is the datastore.

## Commands

```powershell
# Virtualenv lives at ./venv (Python 3.13)
venv\Scripts\pip install -r requirements.txt

# Run dev server (either one)
venv\Scripts\python run.py                      # reload enabled, port 8000
venv\Scripts\python -m uvicorn main:app --reload

# Reset / reseed the database (optional — startup auto-seeds if empty)
venv\Scripts\python init_db.py
```

Interactive API docs at `/docs` (Swagger) once running. There is no test suite.

**Config:** `config.py` loads `.env` via python-dotenv (see `.env.example`). Everything has defaults; `DATABASE_URL` defaults to `sqlite:///./forecast.db`. `SHOW_TOUR_TO_ALL=1` shows the dashboard's onboarding tour + risk disclaimer on every visit (testing); `0`/unset shows it to first-time visitors only (tracked via the `fininteger_tour_done` localStorage key — the tour lives at the bottom of `index.html`).

## Architecture

**Flat module layout at the repo root:** `main.py` (app + lifespan + `/health`), `config.py`, `database.py` (engine/`SessionLocal`/`get_db`), `models.py` (SQLAlchemy: `Instrument`, `ForecastCache`), `schemas.py` (Pydantic response models), `routes/pages.py` (Jinja2 HTML pages), `routes/api.py` (JSON API), `forecaster/ml_engine.py` (the ML pipeline — framework-agnostic). Templates live in `forecaster/templates/forecaster/` and are rendered with `Jinja2Templates`.

**SQLite (`forecast.db`) holds two tables:**
- `instruments` — display metadata, seeded from `INSTRUMENTS` in [init_db.py](init_db.py). The app auto-seeds on startup if the table is empty (`seed_instruments` in lifespan); `python init_db.py` force-reseeds.
- `forecast_cache` — one row per symbol (`UNIQUE(symbol)`), full forecast JSON + `expires_at` (600s TTL). `api_forecast` updates the existing row in place; **do not use `db.merge()` here** — the autoincrement PK makes merge INSERT and violates the unique constraint on refresh.

**Adding/removing an instrument requires three edits:** `INSTRUMENTS` in `init_db.py`, `SYMBOL_MAP` in [forecaster/ml_engine.py](forecaster/ml_engine.py), and `BASE_PRICES` in `_demo_forecast` (offline fallback). Then rerun `python init_db.py`.

**Key-name mapping:** DB columns are `category`/`volume`/`market_cap`, but the frontend JS expects the original short keys `cat`/`vol`/`mcap`. `get_instruments()` in [routes/pages.py](routes/pages.py) does the mapping when embedding instruments into templates. Note `/api/instruments` returns the long DB names (the frontend doesn't fetch it — pages get instruments embedded server-side).

**Request flow for forecasts:**
1. `GET /api/forecast/{symbol}` → check `forecast_cache` row; if fresh, return it.
2. On miss/expiry, `ml_engine.forecast_with_fallback`: fetch 2y of daily OHLCV from yfinance → engineer ~40 technical-indicator features (`_add_features`) → train one XGBRegressor per horizon (1d/1w/1m, predicting forward log return) → build response with forecasts, sentiment, signal bars, technical signals, market data.
3. If yfinance fails (no network / rate limit), it silently falls back to `_demo_forecast` — deterministic pseudo-random data (seeded by symbol + 10-minute window) with the **same response shape** plus `"demo_mode": true`. Any change to the real response structure must be mirrored in `_demo_forecast` AND in `schemas.ForecastData`, or responses break.

Models are trained per-request (nothing persisted); the SQLite cache is the only thing keeping this responsive.

**API endpoints are sync `def` on purpose** — model training and yfinance calls block for seconds, so FastAPI must run them in its threadpool. Don't convert them to `async def` without moving the blocking work to an executor.

**Frontend:** each template is a fully self-contained page — Tailwind via CDN with an inline `tailwind.config` (shared palette: `bg`, `surface`, `accent`, `gain`, `loss`, …), inline CSS, inline vanilla JS consuming the JSON APIs. No base template, no build step; shared styling changes must be replicated across all six templates. Brand images (∫F icon, favicons, lockup) are in `static/images/`, mounted at `/static`. Brand palette if new assets are ever needed: Navy `#0A1B3A`, Electric Blue `#2E6CF6`, Light Blue `#56A8FF`; type: Space Grotesk.

## Gotchas

- `requirements.txt` is UTF-16 encoded — pip reads it fine, but grep/tooling may not.
- Frontend fetches use trailing slashes (`/api/forecast/BTC/`) while routes are declared without; Starlette's `redirect_slashes` bridges this with a 307 per call. Keep it enabled.
- `ml_engine.py` flattens yfinance's MultiIndex columns in `_fetch_ohlcv`; yfinance API changes tend to break there first.
- Cache timestamps are naive UTC (`datetime.utcnow()`) compared in Python — stay consistent if touching them.
- Confidence values are heuristics derived from validation MAPE (clamped 40–95), not calibrated probabilities.
- `forecast.db` is gitignored (untracked on purpose); don't commit it.
