"""
Configuration settings for FastAPI app.
Uses environment variables via python-dotenv
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Environment variables
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./forecast.db")

# Cache settings (in seconds)
FORECAST_CACHE_TTL = 600

# User tour / disclaimer: "1" shows it to ALL users on every visit (testing),
# "0" (default) shows it only to first-time visitors (tracked in localStorage)
SHOW_TOUR_TO_ALL = os.getenv("SHOW_TOUR_TO_ALL", "0") == "1"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# App metadata
APP_NAME = "fininteger"
APP_VERSION = "1.0.0"
