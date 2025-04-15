import os
import importlib
from fastapi import FastAPI

app = FastAPI()

route_dir = os.path.join(os.path.dirname(__file__), "storage")

for filename in os.listdir(route_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"storage.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)