import os
import importlib.util
import inspect
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict

app = FastAPI()

TOOLS = {}

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# Discover *_tool.py files
tool_files = [f for f in os.listdir(TOOLS_DIR) if f.endswith('_tool.py')]

def get_main_callable(module):
    # Prefer 'run', then 'main', then any callable
    for name in ['run', 'main']:
        if hasattr(module, name) and callable(getattr(module, name)):
            return getattr(module, name), name
    # Fallback: first callable
    for name, obj in inspect.getmembers(module):
        if callable(obj) and not name.startswith('__'):
            return obj, name
    return None, None

for tool_file in tool_files:
    tool_name = tool_file.replace('_tool.py', '')
    module_path = os.path.join(TOOLS_DIR, tool_file)
    spec = importlib.util.spec_from_file_location(tool_name, module_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        main_func, func_name = get_main_callable(module)
        if main_func:
            sig = inspect.signature(main_func)
            TOOLS[tool_name] = {
                'module': module,
                'func': main_func,
                'func_name': func_name,
                'signature': sig
            }

@app.get("/")
def list_tools():
    return {
        "tools": [
            {
                "tool": name,
                "endpoint": f"/{name}",
                "parameters": [
                    {
                        "name": param.name,
                        "type": str(param.annotation),
                        "default": param.default if param.default != inspect.Parameter.empty else None
                    }
                    for param in tool['signature'].parameters.values()
                ]
            }
            for name, tool in TOOLS.items()
        ]
    }

# Dynamically add endpoints for each tool
def make_tool_endpoint(tool_name, tool):
    async def endpoint(request: Request):
        params = await request.json() if request.method == 'POST' else dict(request.query_params)
        # Convert params to correct types
        func_params = {}
        for name, param in tool['signature'].parameters.items():
            if name in params:
                value = params[name]
                # Try to cast to the right type
                if param.annotation != inspect.Parameter.empty and param.annotation != str:
                    try:
                        value = param.annotation(value)
                    except Exception:
                        pass
                func_params[name] = value
            elif param.default != inspect.Parameter.empty:
                func_params[name] = param.default
            else:
                return JSONResponse({"error": f"Missing required parameter: {name}"}, status_code=400)
        try:
            if inspect.iscoroutinefunction(tool['func']):
                result = await tool['func'](**func_params)
            else:
                result = tool['func'](**func_params)
            return {"result": result}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
    endpoint.__name__ = f"{tool_name}_endpoint"
    app.add_api_route(f"/{tool_name}", endpoint, methods=["POST", "GET"])

for name, tool in TOOLS.items():
    make_tool_endpoint(name, tool)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
