from fastapi import FastAPI
from easy_pil import Editor, Canvas, Font
from io import BytesIO

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the root route!"}

@app.get("/rankcard")
def rank(avatar: str, username: str, level: str, req: str, xp: str):

    background = Editor(Canvas((800, 200), color="#23272a"))

    avatar_response = requests.get(avatar)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Khong tai duoc anh dai dien.")
    profile = Editor(BytesIO(avatar_response.content)).resize((120, 120)).circle_image()

    background.paste(profile, (15, 14))

    card_right_shape = [(520, 0), (750, 300), (900, 300), (900, 0)]
    background.polygon(card_right_shape, "ff0000")

    # Đường trắng
    background.rectangle((15, 148), width=608, height=35, fill="ffffff", radius=17)

    req = float(req)
    xp = float(xp)
    porcentaje = (xp / req) * 100
    porcentaje = int(min(porcentaje, 100))

    # Áp dụng tỷ lệ phần trăm cho thanh
    background.bar((15, 148), max_width=608, height=35, percentage=porcentaje, fill="00e500", radius=17)

    # Dòng bên dưới văn bản op
    background.rectangle((150, 80 + 4), width=145, height=2, fill="ff0000")

    poppins = Font.poppins(size=35)
    background.text((150, 37 + 4), f"username", font=poppins, color="white")

    poppins = Font.poppins(size=25)
    background.text((145, 107), f"Level: {int(level)}    " f"XP: {abreviar_numero(int(xp))} / {abreviar_numero(int(req))}", font=poppins, color="white")

    img_buffer = BytesIO()
    background.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return Response(content=img_buffer.getvalue(), media_type="image/png")
    
