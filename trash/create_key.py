from fastapi import APIRouter, Request, HTTPException
import secrets
import json
import os
import datetime

router = APIRouter()
file_path = "./storage/api_key.json"

def create_api_key(exp):
    api_key = secrets.token_urlsafe(32)
    api_keys = load_api_keys()
    api_keys.append({
        "api_key": api_key,
        "exp": datetime.date.today().toordinal() + exp
    })
    save_api_keys(api_keys)
    return api_key

def load_api_keys():
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_api_keys(api_keys):
    with open(file_path, "w") as f:
        json.dump(api_keys, f)

def check_api_key(api_key):
    api_keys = load_api_keys()
    for key in api_keys:
        if key["api_key"] == api_key:
            if key["exp"] < datetime.date.today().toordinal():
                api_keys.remove(key)
                save_api_keys(api_keys)
                return False
            else:
                key["exp"] = datetime.date.today().toordinal() + 1
                save_api_keys(api_keys)
                return True
    return False

@router.post("/api/key")
async def create(request: Request):
    data = await request.json()
    exp = data["exp"]
    api_key = create_api_key(exp)
    return {"key": api_key}

@rouyer.get("/api/key")
async def check(request: Request):
    api_key = request.headers.get("key")
    if check_api_key(api_key):
        return {"message": "API key hợp lệ"}
    else:
        raise HTTPException(status_code=401, detail="API key không hợp lệ hoặc đã hết hạn")

