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
    fonts = [ImageFont.load_default(), ImageFont.truetype("arial.ttf", 20), ImageFont.truetype("times.ttf", 20)]
    font = random.choice(fonts)
    x = 50
    y = 30
    for char in captcha_text:
        draw.text((x, y), char, font=font, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        x += 20
        y += random.randint(-5, 5)
    for _ in range(500):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image = image.rotate(random.randint(-10, 10), expand=False)
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
async def captcha():
    captcha = create_captcha()
    return captcha
