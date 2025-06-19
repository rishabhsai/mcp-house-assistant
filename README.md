# MCP House Assistant

A modular AI-powered assistant server that exposes market recap and weather tools as HTTP API endpoints using FastAPI.

## Features
- **Auto-discovers tools**: Any Python file ending with `_tool.py` is exposed as an API endpoint.
- **Parameter introspection**: Endpoints automatically document and validate their parameters.
- **Supports both sync and async tools**.
- **Ready for AI or programmatic use.**

## Setup
1. **Clone the repository and enter the project directory:**
   ```bash
   cd "MCP hiouse assistant"
   ```
2. **(Recommended) Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn yfinance requests
   ```

## Running the Server
```bash
python server.py
```
The server will start at `http://localhost:8000/`.

## API Endpoints
- **GET /**: Lists all available tools and their parameters.
- **POST /market_recap**: Get a market recap.
  - Parameters:
    - `date` (str, optional): Date in YYYY-MM-DD format.
    - `markets` (str, optional): Comma-separated market symbols (e.g., `^GSPC,^IXIC`).
- **POST /weather**: Get weather and forecast.
  - Parameters:
    - `location` (str, required): City or location name.
    - `units` (str, optional): `metric`, `imperial`, or `kelvin` (default: `metric`).
    - `forecast_days` (int, optional): Number of forecast days (default: 1).
    - `api_key` (str, optional): Weather API key (see below).

**Example:**
```bash
curl -X POST "http://localhost:8000/market_recap" -H "Content-Type: application/json" -d '{"date":"2024-06-01","markets":"^GSPC,^IXIC"}'

curl -X POST "http://localhost:8000/weather" -H "Content-Type: application/json" -d '{"location":"London","api_key":"YOUR_API_KEY"}'
```

### Expected Output

#### `/market_recap` Example Response
```json
{
  "result": {
    "date": "2024-06-01",
    "markets": [
      {
        "symbol": "^GSPC",
        "name": "S&P 500",
        "close": 5980.87,
        "change": -1.85,
        "pct_change": -0.03
      },
      {
        "symbol": "^IXIC",
        "name": "NASDAQ Composite",
        "close": 19546.27,
        "change": 25.18,
        "pct_change": 0.13
      }
    ]
  }
}
```

#### `/weather` Example Response
```json
{
  "result": {
    "location": "London, England, United Kingdom",
    "current": {
      "temperature": 18.2,
      "temperature_unit": "°C",
      "feels_like": 17.5,
      "humidity": 65,
      "description": "Partly cloudy",
      "wind_speed": 12.3,
      "wind_unit": "km/h",
      "wind_direction": "SW",
      "pressure": 1012,
      "uv_index": 5,
      "visibility": 10,
      "visibility_unit": "km",
      "cloud_cover": 40,
      "last_updated": "2024-06-01 14:00"
    },
    "forecast": [
      {
        "date": "2024-06-01",
        "high": 20.1,
        "low": 12.3,
        "temperature_unit": "°C",
        "description": "Partly cloudy",
        "rain_chance": 10,
        "snow_chance": 0,
        "max_wind": 15.0,
        "avg_humidity": 60,
        "uv_index": 5
      }
    ]
  }
}
```

## Running Tests
Tests are located in the `tests/` directory. To run all tests:
```bash
python -m unittest discover tests
```

## Weather API Key
3fa75fd7b40144c593f92101251806
```
