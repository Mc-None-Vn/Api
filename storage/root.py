from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse

router = APIRouter()

@router.get("/")
async def root():
    html = """
    <html>
        <head>
            <title>My API Docs</title>
        </head>
        <body>
            <h1>Welcome to my API docs</h1>
        </body>
    </html>
    """
    try:
        return HTMLResponse(content=html)
    except Exception as e:
        return JSONResponse({"error": e}, status_code=500)
