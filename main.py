import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from trie import Trie

app = FastAPI()

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "").split(',')
allowed_origins = allowed_origins if allowed_origins else ["*"]
clear_password = os.environ.get("CLEAR_PASSWORD", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

public_trie = Trie()
words_list_trie = Trie()

with open('data/verbos', 'r') as file:
    words_list = file.read().split('\n')

for word in words_list:
    words_list_trie.insert(word)

@app.get("/match/{word}")
def match(word: str):
    results = words_list_trie.matches(word)
    return {
        "length": len(results),
        "results": results
    }

@app.post("/insert/{word}")
def insert(word: str):

    public_trie.insert(word.strip())

@app.post("/clear")
def clear():
    public_trie.clear()

@app.get("/tree")
def generate_tree():
    return public_trie.get_tree()
