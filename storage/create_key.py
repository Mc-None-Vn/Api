from fastapi import APIRouter, Request, HTTPException
import json
import os
import secrets

router = APIRouter()
file_path = "./storage/data.json"

if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        json.dump([], f)

@router.post("/api/key")
async def key(request: Request):
    data = await request.json()
    if "author" not in data:
        raise HTTPException(status_code=400, detail="Thiếu trường author")

    with open(file_path, "r") as f:
        existing_data = json.load(f)

    for item in existing_data:
        if item["author"] == data["author"]:
            raise HTTPException(status_code=400, detail="Author đã tồn tại")

    api_key = secrets.token_urlsafe(32)
    new_data = {
        "author": data["author"],
        "api_key": api_key,
        "block": False
    }
    existing_data.append(new_data)

    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=4)

    return {"author": new_data["author"], "api_key": new_data["api_key"]}
