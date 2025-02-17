import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.public_tree import router as public_tree_router
from routes.words_list_tree import router as words_list_router
import logging

allowed_origins = os.environ.get("ALLOWED_ORIGINS").split(',')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Allowed origins: {allowed_origins}")

app = FastAPI(title="TrieView")

app.include_router(public_tree_router, prefix="/public_tree", tags=["Public Tree"])
app.include_router(words_list_router, prefix="/words_list", tags=["Words List"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"What is Love?": "https://www.youtube.com/watch?v=i0p1bmr0EmE"}
