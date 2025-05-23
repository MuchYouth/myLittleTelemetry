# backend/app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .routers.upload import router as upload_router

app = FastAPI(title="YML Upload API")

BASE_DIR     = os.path.dirname(__file__)  # …/backend/app
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir))

# 이제 PROJECT_ROOT 에서 한 번만 frontend 폴더에 접근
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend", "assets")),
    name="assets",
)
app.mount(
    "/css",
    StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend", "css")),
    name="css",
)
app.mount(
    "/js",
    StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend", "js")),
    name="js",
)
app.mount(
    "/html",
    StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend")),
    name="html",
)

# app.mount(
#     "/",
#     StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend"), html=True),
#     name="frontend",
# )

app.include_router(upload_router, prefix="/api")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(PROJECT_ROOT, "frontend", "index.html"))
