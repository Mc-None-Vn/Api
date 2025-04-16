from fastapi import APIRouter, Request
from PIL import Image, ImageDraw
from io import BytesIO
from fastapi.responses import Response

router = APIRouter()

# Vị trí cố định cho từng ô
positions = {
    1: (50, 50),
    2: (200, 50),
    3: (350, 50),
    4: (50, 200),
    5: (200, 200),
    6: (350, 200),
    7: (50, 350),
    8: (200, 350),
    9: (350, 350),
}

# Ảnh nền
background_img = Image.new('RGB', (500, 500), color = (73, 109, 137))

# Hàm vẽ X
def draw_x(draw, position):
    x, y = position
    draw.line([(x-20, y-20), (x+20, y+20)], fill=(255, 0, 0), width=10)
    draw.line([(x+20, y-20), (x-20, y+20)], fill=(255, 0, 0), width=10)

# Hàm vẽ O
def draw_o(draw, position):
    x, y = position
    draw.ellipse([(x-20, y-20), (x+20, y+20)], outline=(0, 255, 0), width=10)

@router.post("/api/ttt")
async def tictactoe(request: Request):
    data = await request.json()
    x_positions = [int(i) for i in data["x"].split(",") if i] if data["x"] else []
    o_positions = [int(i) for i in data["o"].split(",") if i] if data["o"] else []

    img = background_img.copy()
    draw = ImageDraw.Draw(img)

    # Vẽ X và O
    for pos in x_positions:
        draw_x(draw, positions[pos])
    for pos in o_positions:
        draw_o(draw, positions[pos])

    # Kiểm tra thắng
    win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7],
    ]
    for condition in win_conditions:
        if all(pos in x_positions for pos in condition):
            # Vẽ đường thắng
            if condition == [1, 2, 3]:
                draw.line([(100, 50), (400, 50)], fill=(0, 0, 255), width=10)
            elif condition == [4, 5, 6]:
                draw.line([(100, 200), (400, 200)], fill=(0, 0, 255), width=10)
            elif condition == [7, 8, 9]:
                draw.line([(100, 350), (400, 350)], fill=(0, 0, 255), width=10)
            elif condition == [1, 4, 7]:
                draw.line([(50, 100), (50, 400)], fill=(0, 0, 255), width=10)
            elif condition == [2, 5, 8]:
                draw.line([(200, 100), (200, 400)], fill=(0, 0, 255), width=10)
            elif condition == [3, 6, 9]:
                draw.line([(350, 100), (350, 400)], fill=(0, 0, 255), width=10)
            elif condition == [1, 5, 9]:
                draw.line([(50, 50), (450, 450)], fill=(0, 0, 255), width=10)
            elif condition == [3, 5, 7]:
                draw.line([(450, 50), (50, 450)], fill=(0, 0, 255), width=10)
            break
        elif all(pos in o_positions for pos in condition):
            # Vẽ đường thắng
            if condition == [1, 2, 3]:
                draw.line([(100, 50), (400, 50)], fill=(0, 0, 255), width=10)
            elif condition == [4, 5, 6]:
                draw.line([(100, 200), (400, 200)], fill=(0, 0, 255), width=10)

    # Lưu hình ảnh vào BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Trả về hình ảnh
    return Response(img_io.read(), media_type="image/png")
