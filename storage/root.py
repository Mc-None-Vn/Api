from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    try:
        return {"message": "Welcome to Mc Api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
