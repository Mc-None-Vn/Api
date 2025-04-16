from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uuid
import os

router = APIRouter()
IMGBB_KEY = os.environ.get("IMGBB_KEY")
EXPIRATION = 60 * 60 * 24  # 1 ngày

class ImgRequest(BaseModel):
    image: str

@router.post("/image/")
async def img(item: ImgRequest):
    try:
        image_data = requests.get(item.image).content
        name = str(uuid.uuid4())
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_KEY,
                "name": name,
                "expiration": EXPIRATION
            },
            files={"image": image_data}
        )

        if response.status_code == 200:
            data = response.json()
            url = data["data"]["url"]
            if not url.endswith(".png"):
                filename, file_extension = os.path.splitext(url)
                url = filename + ".png"            
            return JSONResponse({"image": item.image, "url": url}, status_code=200)
        else:
            return JSONResponse({"error": "Lỗi khi tải hình ảnh lên kho lưu trữ đám mây"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
