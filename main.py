import os
import importlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

with open("./storage/data.json") as d:
    data = json.load(d)

app = FastAPI(
    title=f"{data['title']}",
    description=f"{data['description']}",
    version=f"{data['version']}",
    docs_url="/website/docs/",
)

NEED_KEY = "private"
NO_KEY = "public"
FOLDER = "api"

with open("./storage/no_key.json") as f:
    exempt_request = json.load(f)

@app.middleware("http")
async def check_header(request: Request, call_next):
    if request.url.path.rstrip("/") in exempt_request:
        return await call_next(request)
    path_parts = request.url.path.split("/")
    if len(path_parts) < 3 or path_parts[1] != FOLDER:
        return await call_next(request)
    api_type = path_parts[2]
    if api_type == NO_KEY:
        return await call_next(request)
    if api_type == NEED_KEY:
        if "key" not in request.headers:
            return JSONResponse({"error": "Missing api key"}, status_code=401)
        if request.headers["key"] != str(os.environ.get("API_Key")):
            return JSONResponse({"error": "Api key does not exist"}, status_code=401)
    return await call_next(request)

def load_routers(directory, prefix=""):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            if prefix:
                module = importlib.import_module(f"{prefix}.{module_name}")
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=f"/{prefix}")
            else:
                module = importlib.import_module(module_name)
                if hasattr(module, "router"):
                    app.include_router(module.router)
        elif os.path.isdir(filepath):
            if filename == FOLDER:
                load_routers(filepath, prefix=filename)
            else:
                load_routers(filepath, prefix=f"{prefix}/{filename}" if prefix else filename)

root_dir = os.path.dirname(__file__)
load_routers(root_dir)
