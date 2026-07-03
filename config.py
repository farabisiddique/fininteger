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
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./forecast.db")

# Cache settings (in seconds)
FORECAST_CACHE_TTL = 600

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# App metadata
APP_NAME = "fininteger"
APP_VERSION = "1.0.0"
