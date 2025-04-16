import os
import importlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

with open('./data.json') as d:
    data = json.load(d)

app = FastAPI(
    title=f"{data['title']}",
    description=f"{data['description']}",
    version=f"{data['version']}",
    docs_url="/docs",
)
with open('no_key.json') as k: 
    exempt_routes = json.load(k)

API_Key = os.environ.get("API_Key")

@app.middleware("http")
async def check_header(request: Request, call_next):
    if request.url.path in exempt_routes:
        return await call_next(request)
    if "key" not in request.headers:
        return JSONResponse({"error": "Missing api key"}, status_code=401)
    if request.headers["key"] != str(API_Key):
        return JSONResponse({"error": "Api key does not exist"}, status_code=401)
    return await call_next(request)

route_dir = os.path.join(os.path.dirname(__file__), "storage")
for filename in os.listdir(route_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"storage.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)