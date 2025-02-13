from fastapi import FastAPI
from trie import Trie

app = FastAPI()

trie = Trie()

@app.get("/")
async def hello():
    return "Hello"