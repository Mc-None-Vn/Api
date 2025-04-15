from fastapi import FastAPI
from pydantic import BaseModel
import requests

class imgbb(BaseModel):
  name: str
  image: str

app = FastAPI()

@app.post("/img/")
async def img(item: imgbb):
  return ("message": {"name": item.name, "image": item.image})
