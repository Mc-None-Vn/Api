from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

router = APIRouter()

@router.get("/")
async def root():
    try:
        with open(os.path.join(os.path.dirname(__file__), "../../storage/data.json")) as f:
            data = json.load(f)
        if 'url' not in data:
            raise HTTPException(status_code=500, detail="URL not found in data.json")
        return RedirectResponse(url=f"{data['url']}/docs")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))