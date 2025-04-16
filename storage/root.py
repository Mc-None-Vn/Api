from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
import json

with open('./data.json') as f:
    data = json.load(f)
    
router = APIRouter()

@router.get("/")
async def root():
    html = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta http-equiv="refresh" content="0; url={data['url']['docs']}">

          	<!-- Hiển thị website -->
          	<meta name="title" content={data['title']}>
          	<meta name="description" content={data['description']}>
          	<meta name="viewport" content="width=device-width, initial-scale=1">
	          <meta name="theme-color" content={data['color']}>
	          <link rel="icon" href={data['logo']}>

          	<!-- Hiển thị ở các nền tảng -->
          	<meta property="og:type" content="website">
          	<meta property="og:site_name" content="Team Mc">
          	<meta property="og:url" content={data['url']['base']}>
          	<meta property="og:title" content={data['title']}>
          	<meta property="og:description" content={data['description']}>

          	<!-- Css / Js -->
            <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
            <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
        </head>
        <body>
        </body>
    </html>
    """
    try:
        return HTMLResponse(content=html)
    except Exception as e:
        return JSONResponse({"error": e}, status_code=500)
