from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import requests
import uuid
import os

app = APIRouter()
IMGBB_KEY = os.environ.get("IMGBB_KEY")
Image_Key = os.environ.get("Image_Key")
EXPIRATION = 60 * 60 * 24  # 1 ngày

class ImgRequest(BaseModel):
    image: str

@app.post("/img/")
async def img(item: ImgRequest, key: str = Header(None)):
    if IMGBB_KEY is None or Image_Key is None:
        raise HTTPException(status_code=500, detail="Biến môi trường không được định nghĩa")
    try:
        if key != Image_Key:
            raise HTTPException(status_code=401, detail="Unauthorized")

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
            return {"image": item.image, "url": url}
        else:
            raise HTTPException(status_code=400, detail="Lỗi khi tải hình ảnh")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
