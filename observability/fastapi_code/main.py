from fastapi import FastAPI, Depends
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}