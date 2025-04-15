from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

@app.get("/")
async def root():
    try:
        return {"message": "Welcome to Mc Api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
