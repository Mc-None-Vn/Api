from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the root route!"}

@app.get("/image")
def image(image: str):
    time = 15552000
    name = "test"
    key = c16ec93af2dfad387e2f685867d4d338
    url = "https://api.imgbb.com/1/upload?expiration=" + time + "&key=" + key + "&image=" + image + "&name=" + name
    req = requests.get(url)
    return req.json()
