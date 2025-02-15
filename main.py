from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.trie import Trie
from models.radix import RadixTree

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


# words_list_trie = Trie()

# with open("data/verbos", "r") as file:
#     words_list = file.read().split("\n")

# for word in words_list:
#     words_list_trie.insert(word)


# @app.get("/match/{word}")
# async def match(word: str):
#     results = words_list_trie.matches(word)
#     return {"length": len(results), "results": results}



