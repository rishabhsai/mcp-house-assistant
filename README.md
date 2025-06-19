# MCP House Assistant

A modular AI-powered assistant that uses OpenAI to interpret natural language queries and route them to the correct tool (market recap or weather).

## 🚦 Usage Modes

- **CLI Tool:** Run queries directly from your terminal.
- **HTTP API Endpoint:** Start a server and send queries via HTTP POST requests.

---

## 🏃 Quick Start

### CLI Tool
Run the CLI and enter your query:
```bash
python mcp_server.py "What's the weather in London?"
```
Or just run:
```bash
python mcp_server.py
```
And enter your query when prompted.

### HTTP API Endpoint
1. Start the server:
   ```bash
   uvicorn mcp_api_server:app --reload
   ```
2. Send a POST request to `/query`:
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What's the weather in London?"}'
   ```
   You will receive a JSON response with the result.

---

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

## 🧪 Running Tests
Tests are located in the `