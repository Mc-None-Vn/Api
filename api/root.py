from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
folder = Jinja2Templates(directory="../website")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return folder.TemplateResponse("index.html", {"request": request})
