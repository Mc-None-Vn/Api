from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def root():
    try:
        return {"message": "Welcome to Mc Api"}
    except Exception as e:
        return JSONResponse({"error": e}, status_code=500)
