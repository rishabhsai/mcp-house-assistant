"""
MCP CLI: Accepts a natural language query from the command line, uses OpenAI to decide which tool to call and with what parameters, then calls the tool and prints the result.
"""
import os
import importlib
import inspect
import sys
from dotenv import load_dotenv
import json

# Use the new OpenAI API
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

def main():
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        print("OpenAI API key required in .env as OPENAI_API_KEY.")
        return
    client = OpenAI(api_key=openai_api_key)

    # Accept query from command line argument or prompt
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your query: ")

    # Use OpenAI to decide which tool and params
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
        print(f"Failed to parse LLM response: {str(e)}\nLLM response: {response}")
        return

    # Validate tool
    if tool_name not in TOOLS:
        print(f"Unknown tool: {tool_name}")
        return
    tool_info = TOOLS[tool_name]
    module = import_tool(tool_info["module"])
    main_func = getattr(module, tool_info["main"])
    # Always inject the real weather API key for the weather tool
    if tool_name == "weather":
        params["api_key"] = os.environ.get("WEATHER_API_KEY")
    # Call tool (handle async if needed)
    if inspect.iscoroutinefunction(main_func):
        import asyncio
        result = asyncio.run(main_func(**params))
    else:
        result = main_func(**params)
    print(json.dumps({"result": result}, indent=2))

if __name__ == "__main__":
    main() 