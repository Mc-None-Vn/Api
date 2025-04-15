from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
import uuid
import os

app = FastAPI()
IMGBB_KEY = os.environ.get("IMGBB_KEY")
Image_Key = os.environ.get("Image_Key")
EXPIRATION = 60 * 60 * 24  # 1 ngày

class ImgRequest(BaseModel):
    image: str

@app.get("/")
async def root():
    try:
        return {"message": "Welcome to Mc Api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/img/")
async def img(item: ImgRequest, key: str = Header(None)):
    try:
        # Kiểm tra header bảo mật
        if key != Image_Key:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Tạo tên ngẫu nhiên cho hình ảnh
        name = str(uuid.uuid4()) + ".png"

        # Tải hình ảnh từ đường link
        image_data = requests.get(item.image).content

        # Post dữ liệu qua API ImgBB
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
            return {"image": image, "url": url}
        else:
            raise HTTPException(status_code=400, detail="Lỗi khi tải hình ảnh")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))