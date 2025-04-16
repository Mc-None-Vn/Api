from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uuid
import os
import re
from dotenv import load_dotenv

load_dotenv()
IMGBB_KEY = os.getenv("IMGBB_KEY")
router = APIRouter()

class ImgRequest(BaseModel):
    image: str
    time: str = "1d"

def parse_time(time_str):
    pattern = r"(\d+)([dDhHmMsS])"
    matches = re.findall(pattern, time_str, re.IGNORECASE)
    seconds = 0
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    for value, unit in matches:
        unit = unit.lower()
        if unit in units:
            seconds += int(value) * units[unit]
        else:
            seconds = 86400
    return seconds

@router.post("/api/image")
async def img(item: ImgRequest):
    try:
        ex = parse_time(item.time)
        name = str(uuid.uuid4())
        key = IMGBB_KEY
        image_data = requests.get(item.image).content
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": key, "name": name, "expiration": ex},
            files={"image": image_data},
        )
        if response.status_code == 200:
            data = response.json()
            url = data["data"]["url"]
            if not url.endswith(".png"):
                filename, file_extension = os.path.splitext(url)
                url = filename + ".png"
            return JSONResponse({"url": url}, status_code=200)
        else:
            return JSONResponse({"error": "Error uploading image to ImgBB"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
