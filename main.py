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
    docs_url="/docs/",
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

route_dir = os.path.join(os.path.dirname(__file__), FOLDER)
for filename in os.listdir(route_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"{FOLDER}.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)

for subfolder in os.listdir(route_dir):
    subfolder_path = os.path.join(route_dir, subfolder)
    if os.path.isdir(subfolder_path):
        for filename in os.listdir(subfolder_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(f"{FOLDER}.{subfolder}.{module_name}")
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=f"/{FOLDER}")
                    