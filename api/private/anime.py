from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uuid
import os

router = APIRouter()

class NekosRequest(BaseModel):
    name: str

@router.post("/anime")
async def anime(item: NekosRequest):
    try:
        while True:
            response = requests.get(f"https://nekos.best/api/v2/{item.name}")
            if response.status_code == 200:
                data = response.json()
                if "results" in data and len(data["results"]) > 0:
                    image_url = data["results"][0]["url"]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        ex = 86400
                        imgbb_name = str(uuid.uuid4())
                        key = os.environ.get("IMGBB_KEY")
                        response_imgbb = requests.post(
                            "https://api.imgbb.com/1/upload",
                            data={"key": key, "name": imgbb_name, "expiration": ex},
                            files={"image": image_response.content},
                        )
                        if response_imgbb.status_code == 200:
                            data_imgbb = response_imgbb.json()
                            url = data_imgbb["data"]["url"]
                            return JSONResponse({"url": url}, status_code=200)
                        else:
                            return JSONResponse({"error": "Error uploading image to ImgBB"}, status_code=400)
                    else:
                        print(f"Image {image_url} not found, trying again...")
                else:
                    return JSONResponse({"error": "No image found"}, status_code=400)
            else:
                return JSONResponse({"error": "Error getting image from Nekos.best"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
