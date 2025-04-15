from fastapi import FastAPI
from storage.root import app as root
from storage.image import app as image

api = FastAPI()

api.include_router(root)
api.include_router(image)