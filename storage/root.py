from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
import json

with open('./data.json') as f:
    data = json.load(f)
    
router = APIRouter()

@router.get("/")
async def root():
    html = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta http-equiv="refresh" content="0; url={data['url']}/docs/">
        </head>
    </html>
    """
    try:
        return HTMLResponse(content=html)
    except Exception as e:
        return JSONResponse({"error": e}, status_code=500)
