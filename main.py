"""
FastAPI application entry point.
Replaces Django's manage.py runserver.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import APP_NAME, APP_VERSION, DEBUG, LOG_LEVEL
from database import init_db, SessionLocal
from routes import api, pages
from forecaster.ml_engine import SYMBOL_MAP
from init_db import seed_instruments

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown event handler."""
    # Startup
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    init_db()
    with SessionLocal() as db:
        added = seed_instruments(db)
        if added:
            logger.info(f"Seeded {added} instruments")
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info(f"Shutting down {APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (brand images live in static/images/)
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")

# Include routers
app.include_router(api.router)
app.include_router(pages.router)

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION,
        "symbols_available": len(SYMBOL_MAP)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )
