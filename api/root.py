from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

router = APIRouter()

@router.get("/")
async def root():
    try:
        with open(os.path.join(os.path.dirname(__file__), "../storage/data.json")) as f:
            data = json.load(f)
        html_content = f"""
        <!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
    <meta name="title" content="">
    <meta name="description" content="">
    <meta name="theme-color" content="">
    <link rel="icon" href="">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="">
    <meta property="og:url" content="">
    <meta property="og:title" content="">
    <meta property="og:description" content="">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="./css/base.css">
    <link rel="stylesheet" href="./css/project.css">
    <script src="./website/js/meta.js"></script>
</head>
<body>
    <script>
        const metaRefresh = document.createElement('meta');
        metaRefresh.httpEquiv = 'refresh';
        metaRefresh.content = `0; url=${data.url}/website/home.html`;
        document.head.appendChild(metaRefresh);
    </script>
</body>
</html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
