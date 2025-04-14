from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the root route!"}

@app.get("/items/")
def items():
    return {"message": "Welcome to the items route!"}

@app.get("/items/update/")
def update_item():
    return {"message": "Welcome to the update item route!"}
