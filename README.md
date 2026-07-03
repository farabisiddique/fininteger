# MAIN-APP: Financial Market Forecasting Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-1F77B4.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-performance financial market forecasting application that predicts crypto, stock, commodity, ETF, and forex price movements using machine learning (XGBoost). Built with FastAPI and SQLite for optimal performance and scalability.

## 🎯 Features

- **Multi-Asset Forecasting**: Support for 20+ financial instruments across 5 categories
- **XGBoost ML Models**: Real-time model training on 2 years of historical data
- **Technical Analysis**: 40+ engineered indicators (RSI, MACD, Bollinger Bands, ATR, Stochastic, etc.)
- **Multi-Horizon Predictions**: 1-day, 1-week, and 1-month price forecasts
- **Sentiment Analysis**: BULLISH / BEARISH / NEUTRAL classification
- **Smart Caching**: 600-second forecast cache with SQLite persistence
- **Offline Mode**: Deterministic fallback forecasts when yfinance is unavailable
- **RESTful API**: Production-ready endpoints with auto-generated documentation
- **Real-time Data**: Live market data via yfinance integration
- **Interactive UI**: Responsive web interface with Tailwind CSS and vanilla JavaScript

## 📊 Supported Assets

### Cryptocurrencies
- Bitcoin (BTC), Ethereum (ETH), Solana (SOL), BNB (BNB), Ripple (XRP)

### Stocks
- Apple (AAPL), NVIDIA (NVDA), Microsoft (MSFT), Tesla (TSLA), Amazon (AMZN)

### Commodities
- Gold (XAU), Silver (XAG), Crude Oil (OIL), Natural Gas (NG)

### ETFs
- SPY (S&P 500), QQQ (Nasdaq-100), VTI (Total Market)

### Forex
- EUR/USD, GBP/USD, USD/JPY

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104+ - Modern, async-first web framework
- **ASGI Server**: Uvicorn - Lightning-fast async HTTP server
- **Database**: SQLite 3 - Lightweight, file-based persistence
- **ORM**: SQLAlchemy 2.0 - SQL toolkit with powerful ORM
- **Validation**: Pydantic 2.5+ - Data validation using Python type hints

### Machine Learning
- **XGBoost 2.0+** - Gradient boosting for regression
- **Scikit-learn** - Feature scaling and evaluation metrics
- **Pandas** - Data manipulation and time series handling
- **NumPy** - Numerical computing

### Data Source
- **yfinance** - Free market data from Yahoo Finance API

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS 3** - Utility-first CSS framework (CDN)
- **JavaScript (Vanilla)** - No framework dependencies
- **Jinja2** - Server-side template rendering

### Development Tools
- **Python 3.10+** - Latest Python runtime
- **pip** - Package management
- **python-dotenv** - Environment configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Internet connection (for yfinance data)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd fininteger
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings (optional for development)
# For production, ensure SECRET_KEY is set to a secure random value
```

5. **Initialize database**
```bash
python init_db.py
```

### Running the Application

**Development mode** (with auto-reload):
```bash
python run.py
```

**Alternative** (direct uvicorn):
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode** (single process):
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at **http://localhost:8000**

### Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | Web interface - Markets overview |
| http://localhost:8000/docs | Interactive API documentation (Swagger UI) |
| http://localhost:8000/redoc | Alternative API documentation (ReDoc) |
| http://localhost:8000/health | System health check |

## 📖 API Documentation

### Interactive Docs
Visit **http://localhost:8000/docs** for a live, interactive API explorer where you can:
- View all endpoints with descriptions
- Try API requests directly in the browser
- See request/response schemas
- Export API specifications

### Key Endpoints

#### Get Forecast
```http
GET /api/forecast/{symbol}
```

**Response** (example: BTC):
```json
{
  "symbol": "BTC",
  "current_price": 67420.50,
  "demo_mode": false,
  "forecasts": {
    "1d": {
      "price": 68500.25,
      "pct_change": 1.60,
      "direction": "up",
      "confidence": 78,
      "mape": 3.45
    },
    "1w": {
      "price": 69800.00,
      "pct_change": 3.54,
      "direction": "up",
      "confidence": 72,
      "mape": 5.21
    },
    "1m": {
      "price": 70150.75,
      "pct_change": 4.08,
      "direction": "up",
      "confidence": 65,
      "mape": 7.89
    }
  },
  "sentiment": "BULLISH",
  "avg_confidence": 72,
  "signal_bars": {
    "trend_strength": 78,
    "volatility": 52,
    "volume_signal": 68,
    "momentum": 74
  },
  "technical_signals": {
    "macd": {"status": "DETECTED", "active": true},
    "rsi": {"status": "OVERBOUGHT", "active": true, "value": 72.5},
    "volume": {"status": "HIGH", "active": true},
    "support": {"status": "CLEAR", "active": false}
  },
  "market_data": {
    "high_24": 68200.00,
    "low_24": 66850.00,
    "open_24": 67100.00,
    "volume": "38.2B",
    "chg_7d": 2.34,
    "rsi": 72.5,
    "bb_pct": 65.3,
    "stoch_k": 78.2
  }
}
```

#### List All Instruments
```http
GET /api/instruments
```

#### Get Current Price
```http
GET /api/price/{symbol}
```

Response:
```json
{
  "symbol": "BTC",
  "price": 67420.50
}
```

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok",
  "app": "MAIN-APP",
  "version": "1.0.0",
  "symbols_available": 20
}
```

## 📁 Project Structure

```
fininteger/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management from .env
├── database.py            # SQLAlchemy database configuration
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic request/response schemas
├── init_db.py             # Database initialization script
├── run.py                 # Development server launcher
│
├── routes/                # API route handlers
│   ├── __init__.py
│   ├── api.py            # /api/* endpoints
│   └── pages.py          # HTML page routes
│
├── forecaster/            # ML forecasting module
│   ├── ml_engine.py      # XGBoost model training & prediction
│   ├── models.py         # SQLAlchemy models (Instrument, ForecastCache)
│   ├── templates/        # HTML templates (Jinja2)
│   │   └── forecaster/
│   │       ├── index.html
│   │       ├── tools.html
│   │       ├── markets.html
│   │       ├── portfolio.html
│   │       ├── about.html
│   │       └── contact.html
│   ├── migrations/       # SQLAlchemy migrations (if needed)
│   ├── tests.py         # Unit tests
│   └── __init__.py
│
├── .env                   # Environment configuration (git ignored)
├── .env.example          # Environment configuration template
├── requirements.txt      # Python dependencies
├── forecast.db          # SQLite database (created on first run)
│
├── README.md            # This file
├── MIGRATION.md         # Django → FastAPI migration notes
├── CHANGES.md           # Detailed change log
└── .gitignore          # Git ignore file
```

## 🗄️ Database Schema

### Instruments Table
Stores metadata for all financial instruments:
```sql
CREATE TABLE instruments (
    id TEXT PRIMARY KEY,                    -- Symbol (e.g., "BTC")
    name TEXT NOT NULL,                     -- Full name
    category TEXT NOT NULL,                 -- Category (crypto/stocks/etc)
    price REAL NOT NULL,                    -- Last known price
    change REAL NOT NULL,                   -- Percentage change
    volume TEXT NOT NULL,                   -- Trading volume
    market_cap TEXT NOT NULL,               -- Market capitalization
    icon TEXT NOT NULL,                     -- Unicode icon
    created_at DATETIME,                    -- Creation timestamp
    updated_at DATETIME                     -- Last update timestamp
);
```

### ForecastCache Table
Stores cached forecast results with TTL:
```sql
CREATE TABLE forecast_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT UNIQUE,                     -- Instrument symbol
    forecast_data JSON NOT NULL,            -- Full forecast JSON
    created_at DATETIME,                    -- Creation timestamp
    updated_at DATETIME,                    -- Last update timestamp
    expires_at DATETIME NOT NULL            -- Cache expiration time
);
```

## 🤖 ML Model Details

### Features (40+)
The model uses 40+ engineered features:
- **Returns**: Log returns at 1, 2, 3, 5, 10, 21 day lags
- **Moving Averages**: SMA (5, 10, 20, 50), EMA (12, 26)
- **Momentum**: MACD, RSI(14), Stochastic K/D
- **Volatility**: Bollinger Bands (20, 2σ), ATR(14)
- **Volume**: Volume MA ratio, OBV, OBV normalized
- **Price Action**: High-low range, Close position, Log close
- **Seasonality**: Day-of-week, Month

### Training
- **Data**: 2 years of daily OHLCV data from yfinance
- **Algorithm**: XGBoost Regressor
- **Target**: Forward log returns (1d/1w/1m horizons)
- **Validation**: 80/20 train/val split with MAPE metric
- **Hyperparameters**: Tuned for stability and low variance

### Confidence Scoring
Confidence = 100 * (1 - validation_MAPE * 5), clamped to [40, 95]
- Lower validation error → Higher confidence
- Not a probability; use with domain knowledge

## 🔧 Configuration

### Environment Variables (.env)
```env
# Security
SECRET_KEY=your-secure-random-key-here

# Deployment
DEBUG=True                                  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///./forecast.db

# Logging
LOG_LEVEL=INFO                             # DEBUG, INFO, WARNING, ERROR
```

### Production Configuration
For production deployments:
1. Set `SECRET_KEY` to a cryptographically secure random string
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use environment-specific database URL
5. Enable HTTPS/SSL certificates
6. Set up monitoring and logging aggregation

## 📊 Adding New Instruments

To add a new instrument:

1. **Update SYMBOL_MAP** in `forecaster/ml_engine.py`:
```python
SYMBOL_MAP = {
    # ... existing entries ...
    "NEW": "TICKER-SYMBOL",
}
```

2. **Update instruments list** in `init_db.py`:
```python
INSTRUMENTS = [
    # ... existing entries ...
    {"id": "NEW", "name": "New Asset", "cat": "category", "price": 0, ...},
]
```

3. **Reinitialize database**:
```bash
python init_db.py
```

## 📈 Performance Considerations

### Caching Strategy
- Forecasts cached for 600 seconds (configurable)
- Cache stored in SQLite for persistence across restarts
- Automatic cache expiration based on `expires_at` timestamp

### Optimization Tips
- First forecast request takes 10-30 seconds (model training)
- Subsequent requests within 600s return cached results (~50ms)
- Use forecasts for the same symbol frequently to benefit from cache
- Monitor yfinance rate limits for high-volume deployments

### Scaling
For production deployments with high load:
- Use connection pooling (SQLAlchemy handles this)
- Deploy with multiple workers: `uvicorn main:app --workers 4`
- Consider Redis cache for distributed deployments
- Use a production database (PostgreSQL) instead of SQLite

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# List instruments
curl http://localhost:8000/api/instruments

# Get forecast (first time takes longer)
curl http://localhost:8000/api/forecast/BTC

# Get current price
curl http://localhost:8000/api/price/ETH
```

### Automated Tests
```bash
# Run test suite (when available)
pytest forecaster/tests.py -v
```

## 📚 Development

### Setting Up Development Environment
```bash
# Clone repository
git clone <repo-url>
cd fininteger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env
cp .env.example .env

# Initialize database
python init_db.py

# Start development server
python run.py
```

### Code Structure
- **main.py**: FastAPI application setup and configuration
- **routes/**: Request handlers organized by resource type
- **models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic request/response validation
- **forecaster/ml_engine.py**: ML model training and prediction logic

### Hot Reload
The development server automatically reloads on code changes. Simply edit files and refresh the browser.

## 🚀 Deployment

### Local Deployment
```bash
python run.py
```

### Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fininteger .
docker run -p 8000:8000 fininteger
```

### Cloud Deployment (Heroku, Railway, Render)
1. Ensure `runtime.txt` specifies Python 3.10+
2. Set environment variables in platform dashboard
3. Platform will install `requirements.txt` automatically
4. Application starts via `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📝 Migration from Django

This project was originally built with Django and has been migrated to FastAPI for:
- **Performance**: 2-3x faster with async/await
- **Type Safety**: Pydantic automatic validation
- **Developer Experience**: Auto-generated API docs
- **Modern Python**: Native async support

See [MIGRATION.md](MIGRATION.md) for detailed migration notes.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and returns
- Add docstrings to functions and classes
- Keep functions focused and modular

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### Port Already in Use
```bash
python -m uvicorn main:app --port 8001
```

### Database Locked
```bash
rm forecast.db
python init_db.py
```

### Module Not Found
```bash
pip install --upgrade -r requirements.txt
```

### yfinance Connection Issues
The application gracefully falls back to demo mode if yfinance is unavailable. Forecasts will still be generated but marked as `demo_mode: true`.

### Performance Issues
- Clear cache: `rm forecast.db && python init_db.py`
- Check yfinance rate limits
- Monitor network connectivity
- Review logs with `LOG_LEVEL=DEBUG`

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check [MIGRATION.md](MIGRATION.md) for common questions
- Review [CHANGES.md](CHANGES.md) for recent updates

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [XGBoost](https://xgboost.readthedocs.io/) - Machine learning
- [yfinance](https://finance.yahoo.com/) - Market data
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Tailwind CSS](https://tailwindcss.com/) - Styling

---

**Made with ❤️ for financial analysis and forecasting**

Last Updated: July 3, 2026
