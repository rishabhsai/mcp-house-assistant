"""
MCP API Server: Exposes a /query POST endpoint that accepts a natural language query, uses OpenAI to decide which tool to call and with what parameters, then calls the tool and returns the result as JSON.
"""
import os
import importlib
import inspect
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI

# Load .env file
load_dotenv()

# Import tool modules
def import_tool(tool_name):
    return importlib.import_module(tool_name)

TOOLS = {
    "market_recap": {
        "module": "market_recap_tool",
        "main": "main",
        "description": "Get a market recap for a given date and markets.",
        "params": ["date", "markets"]
    },
    "weather": {
        "module": "weather_tool",
        "main": "main",
        "description": "Get weather and forecast for a location.",
        "params": ["location", "units", "forecast_days", "api_key"]
    }
}

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def mcp_query(req: QueryRequest):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        return JSONResponse({"error": "OpenAI API key required in .env as OPENAI_API_KEY."}, status_code=400)
    client = OpenAI(api_key=openai_api_key)

    user_query = req.query
    system_prompt = (
        "You are an AI orchestrator. Given a user query, decide which tool to call and extract the parameters. "
        "Available tools: "
        "market_recap(date: str, markets: str) - date in YYYY-MM-DD, markets as comma-separated symbols. "
        "weather(location: str, units: str = 'metric', forecast_days: int = 1, api_key: str) - units can be 'metric', 'imperial', or 'kelvin'. "
        "Respond in JSON: {\"tool\": ..., \"params\": {...}}. "
        "If unsure, make your best guess."
    )
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )
    try:
        tool_call = response.choices[0].message.content
        # Remove code block markers if present
        if tool_call:
            tool_call = tool_call.strip()
            if tool_call.startswith('```'):
                tool_call = tool_call.split('\n', 1)[1].rsplit('```', 1)[0]
            tool_call = tool_call.strip()
        tool_call = json.loads(tool_call)
        tool_name = tool_call["tool"]
        params = tool_call["params"]
    except Exception as e:
        return JSONResponse({"error": f"Failed to parse LLM response: {str(e)}", "llm_response": str(response)}, status_code=500)

    # Validate tool
    if tool_name not in TOOLS:
        return JSONResponse({"error": f"Unknown tool: {tool_name}"}, status_code=400)
    tool_info = TOOLS[tool_name]
    module = import_tool(tool_info["module"])
    main_func = getattr(module, tool_info["main"])
    # Always inject the real weather API key for the weather tool
    if tool_name == "weather":
        params["api_key"] = os.environ.get("WEATHER_API_KEY")
    # Call tool (handle async if needed)
    if inspect.iscoroutinefunction(main_func):
        import asyncio
        result = await main_func(**params)
    else:
        result = main_func(**params)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 