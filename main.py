import os
import importlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

def load_data(file_path):
    with open(file_path) as f:
        return json.load(f)

def fast_api(data):
    return FastAPI(
        title=data['title'],
        description=data['description'],
        version=data['version'],
        docs_url="/website/docs/",
    )

def run_router(app, folder):
    for FOLDER in folder:
        route_dir = os.path.join(os.path.dirname(__file__), FOLDER)
        for filename in os.listdir(route_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(f"{FOLDER}.{module_name}")
                if hasattr(module, "router"):
                    try:
                        app.include_router(module.router)
                    except Exception as e:
                        print(f"Lỗi khi include router {module_name}: {e}")
        for subfolder in os.listdir(route_dir):
            subfolder_path = os.path.join(route_dir, subfolder)
            if os.path.isdir(subfolder_path):
                for filename in os.listdir(subfolder_path):
                    if filename.endswith(".py") and filename != "__init__.py":
                        module_name = filename[:-3]
                        module = importlib.import_module(f"{FOLDER}.{subfolder}.{module_name}")
                        if hasattr(module, "router"):
                            try:
                                app.include_router(module.router, prefix=f"/{FOLDER}/{subfolder}")
                            except Exception as e:
                                print(f"Lỗi khi include router {module_name}: {e}")

data = load_data("./storage/data.json")
exempt_request = load_data("./storage/no_key.json")

app = fast_api(data)

@app.middleware("http")
async def check_header(request: Request, call_next):
    if request.url.path.rstrip("/") in exempt_request:
        return await call_next(request)

    path_parts = request.url.path.split("/")
    if len(path_parts) < 3 or path_parts[1] != "api":
        return await call_next(request)

    api_type = path_parts[2]
    if api_type == "public":
        return await call_next(request)

    if api_type == "private":
        if "key" not in request.headers:
            return JSONResponse({"error": "Missing api key"}, status_code=401)
        if request.headers["key"] != str(os.environ.get("API_Key")):
            return JSONResponse({"error": "Api key does not exist"}, status_code=401)
    return await call_next(request)

FOLDERS = ["api"]
run_router(app, FOLDERS)

