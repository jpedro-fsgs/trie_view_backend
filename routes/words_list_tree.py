import logging
from fastapi import APIRouter, HTTPException

from models.radix import RadixTree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

words_list_radix = RadixTree()

@router.post("/add_list")
async def add():
    if len(words_list_radix.root.children) > 0:
        raise HTTPException(status_code=400, detail="Tree not empty")
    with open("data/pt_br_50k_split.txt", "r") as file:
        words_list = file.read().splitlines()

    for i, word in enumerate(words_list, start=1):
        words_list_radix.insert(word.split(' ')[0])
        if i % 100000 == 0:
            logger.info(f"{i} added words")

    logger.info(f"{i} added words")
    return {"detail": f"{i} words added successfully"}


@router.post("/clear_tree")
async def clear_tree():
    words_list_radix.clear()
    logger.info("Tree cleared")
    return {"detail": "Tree cleared successfully"}



@router.get("/matches/{word}")
async def matches(word: str):
    word = word.strip().lower()
    if len(word) < 3:
        return {"length": 0, "words": []}

    result = words_list_radix.matches(word)

    return {"length": len(result), "words": result}
