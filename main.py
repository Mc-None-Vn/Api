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

root_dir = os.path.dirname(__file__)
for filename in os.listdir(root_dir):
    filepath = os.path.join(root_dir, filename)
    if os.path.isfile(filepath) and filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            app.include_router(module.router)
    elif os.path.isdir(filepath) and filename == FOLDER:
        api_dir = filepath
        for api_filename in os.listdir(api_dir):
            api_filepath = os.path.join(api_dir, api_filename)
            if os.path.isfile(api_filepath) and api_filename.endswith(".py") and api_filename != "__init__.py":
                module_name = api_filename[:-3]
                module = importlib.import_module(f"{FOLDER}.{module_name}")
                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=f"/{FOLDER}")
            elif os.path.isdir(api_filepath):
                for sub_api_filename in os.listdir(api_filepath):
                    if sub_api_filename.endswith(".py") and sub_api_filename != "__init__.py":
                        module_name = sub_api_filename[:-3]
                        module = importlib.import_module(f"{FOLDER}.{api_filename}.{module_name}")
                        if hasattr(module, "router"):
                            app.include_router(module.router, prefix=f"/{FOLDER}/{api_filename}")
                            