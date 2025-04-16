from fastapi import APIRouter, Request
from PIL import Image
from io import BytesIO
import requests
from fastapi.responses import Response

router = APIRouter()

@router.post("/api/ttt")
async def ttt(request: Request):
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

    # Lưu hình ảnh vào BytesIO
    img_io = BytesIO()
    background_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Trả về hình ảnh
    return Response(img_io.read(), media_type="image/png")
    