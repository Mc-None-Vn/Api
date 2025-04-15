from fastapi import FastAPI
from pydantic import BaseModel
import requests

class imgbb(BaseModel):
  name: str
  image: str

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Welcome to Mc Api"}

@app.post("/img/")
async def img(item: imgbb):
  return ("message": {"name": item.name, "image": item.image})
