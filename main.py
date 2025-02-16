from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.public_tree import router as public_tree_router

app = FastAPI(title="TrieView")

app.include_router(public_tree_router, prefix="/public_tree", tags=["Public Tree"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"What is Love?": "https://www.youtube.com/watch?v=i0p1bmr0EmE"}
