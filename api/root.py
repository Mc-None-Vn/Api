from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="../website")

@router.get("/")
async def read_root(request: Request):
    with open(os.path.join(os.path.dirname(__file__), "../storage/data.json")) as f:
        data = json.load(f)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})