from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.database import database
from src.routers.post import post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)
