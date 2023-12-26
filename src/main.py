from fastapi import FastAPI

from routers.post import post_router

app = FastAPI()
app.include_router(post_router)
