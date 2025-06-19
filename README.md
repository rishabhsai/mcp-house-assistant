# MCP House Assistant

A modular AI-powered assistant that uses OpenAI to interpret natural language queries and route them to the correct tool (market recap or weather) via a command-line interface.

## 🚀 How It Works
- **Natural Language Interface:** Ask questions like "What's the weather in London?" or "Give me a market recap for today".
- **LLM Orchestration:** Uses OpenAI's GPT-4o to decide which tool to call and with what parameters.
- **Tool Execution:** Calls the appropriate Python tool and prints the result as JSON.
- **No Web Server Needed:** Everything runs from the command line. (The old FastAPI server is deprecated and has been removed.)

## 🛠️ Tools
- **Market Recap Tool:** Fetches market data for major indices or specified symbols for a given date.
- **Weather Tool:** Fetches current weather and forecast for a given location using WeatherAPI.

## 🗝️ Setup
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
   pip install -r requirements.txt
   # Or, if requirements.txt is missing:
   pip install openai python-dotenv yfinance requests
   ```
4. **Set up your .env file:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   WEATHER_API_KEY=your_weatherapi_key_here
   ```
   Replace with your actual API keys.

## 🏃 Usage
Run the MCP CLI and enter your query:
```bash
python mcp_server.py "What's the weather in London?"
```
Or just run:
```bash
python mcp_server.py
```
And enter your query when prompted.

### Example Output
```json
{
  "result": {
    "location": "London, City of London, Greater London, United Kingdom",
    "current": {
      "temperature": 31.1,
      "temperature_unit": "°C",
      "feels_like": 31.5,
      "humidity": 31,
      "description": "Sunny",
      ...
    },
    "forecast": [ ... ]
  }
}
```

## 🧪 Running Tests
Tests are located in the `tests/` directory. To run all tests:
```bash
python -m unittest discover tests
```

## 📝 Notes
- The CLI will always use your real API keys from `.env` for tool calls, regardless of LLM output.
- You can add more tools by following the `_tool.py` pattern and adding a `main` function.
