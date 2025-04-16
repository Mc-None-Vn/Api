from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api")
async def api():
    try:
        return JSONResponse({"message": "Welcome to Mc Api"}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": e}, status_code=500)
