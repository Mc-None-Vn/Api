from fastapi import APIRouter, Request
from PIL import Image
from io import BytesIO
import requests
from fastapi.responses import Response, JSONResponse
import uuid
import os

router = APIRouter()

# Thư mục lưu hình ảnh
image_dir = "storage"

# Tạo thư mục nếu nó không tồn tại
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

@router.post("/api/storage/")
async def storage(request: Request):
    data = await request.json()
    background_url = data["background"]
    images = data["image"]

    # Tải ảnh nền
    background_response = requests.get(background_url)
    background_img = Image.open(BytesIO(background_response.content))

    # Ghép ảnh
    for image_data in images:
        image_url = image_data["url"]
        x, y = map(int, image_data["coord"])

        # Tải ảnh
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        # Tính toán vị trí ghép ảnh
        paste_x = x
        paste_y = y

        # Ghép ảnh
        background_img.paste(image, (paste_x, paste_y))

    # Lưu hình ảnh vào thư mục
    image_id = str(uuid.uuid4())
    image_path = f"{image_dir}/{image_id}.png"
    background_img.save(image_path)

    # Trả về link đến hình ảnh
    image_url = f"/api/storage/{image_id}.png"
    return JSONResponse(content={"image_url": image_url}, status_code=200)
