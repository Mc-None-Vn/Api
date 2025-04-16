import os
import importlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

with open("./data.json") as d:
    data = json.load(d)

app = FastAPI(
    title=f"{data['title']}",
    description=f"{data['description']}",
    version=f"{data['version']}",
    docs_url="/docs/",
)

@app.middleware("http")
async def check_header(request: Request, call_next):
    try:
        with open("./no_key.json") as f:
            exempt_paths = json.load(f)
    except FileNotFoundError:
        exempt_paths = []

    if request.url.path.rstrip("/") in exempt_paths:
        return await call_next(request)

    if "author" not in request.headers or "key" not in request.headers:
        return JSONResponse({"error": "Missing author / api key"}, status_code=401)

    author = request.headers["author"]
    api_key = request.headers["key"]

    try:
        with open("./storage/data.json") as f:
            users = json.load(f)
    except FileNotFoundError:
        return JSONResponse({"error": "User data not found"}, status_code=500)

    user = next((user for user in users if user["author"] == author and user["api_key"] == api_key), None)
    if user is None:
        return JSONResponse({"error": "Author / api key is incorrect"}, status_code=401)

    if user["block"]:
        return JSONResponse({"error": "Account has been blocked"}, status_code=403)

    return await call_next(request)

route_dir = os.path.join(os.path.dirname(__file__), "storage")
for filename in os.listdir(route_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"storage.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)
