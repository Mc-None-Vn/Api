from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../website")

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})