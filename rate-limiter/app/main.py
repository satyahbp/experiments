from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from routes import router
from core.database import init_db
from core.middleware import CustomMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    root_path="/api",
    lifespan=lifespan
)
app.add_middleware(CustomMiddleware)

Instrumentator().instrument(app).expose(app)

app.include_router(router, prefix="/v1")

@app.get("/")
def home():
    return {"message": "Hello World"}

