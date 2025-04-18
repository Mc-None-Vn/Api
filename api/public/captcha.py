from fastapi import APIRouter
import random
import string
from PIL import Image, ImageDraw, ImageFont
import requests
import base64
from io import BytesIO
import uuid
import os

router = APIRouter()

def generate_captcha(length=6):
    characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(length))
    return captcha_text

def generate_captcha_image(captcha_text):
    width, height = 200, 100
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((50, 30), captcha_text, font=font, fill=(0, 0, 0))
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(0, 0, 0))
    return image

def upload_image_to_imgbb(image):
    try:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        imgbb_name = str(uuid.uuid4())
        key = os.environ.get("IMGBB_KEY")
        ex = 86400
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": key, "name": imgbb_name, "expiration": ex},
            files={"image": buffer},
        )
        response.raise_for_status()
        return response.json()["data"]["url"]
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi upload ảnh: {e}")
        return None

def create_captcha():
    captcha_text = generate_captcha()
    image = generate_captcha_image(captcha_text)
    image_url = upload_image_to_imgbb(image)
    return {"url": image_url, "code": captcha_text} 

@router.get("/captcha")
def get_captcha():
    captcha = create_captcha()
    return captcha
