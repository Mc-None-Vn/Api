from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
class Items = BaseModel():
    name: str
    avt: str

@app.get("/")
def root():
    return {"message": "Welcome to the root route!"}

@app.port("/image")
def image(item: Items):
    time = 15552000
    name = item.name
    image = item.image
    key = c16ec93af2dfad387e2f685867d4d338
    url = "https://api.imgbb.com/1/upload?expiration=" + time + "&key=" + key + "&image=" + image + "&name=" + name
    req = requests.get(url)
    return req.json()
