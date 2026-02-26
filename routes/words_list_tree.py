import logging
import os
from fastapi import APIRouter, HTTPException

from models.radix import RadixTree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

words_list_radix = RadixTree()
snapshot_path = os.environ.get("WORDS_LIST_RADIX_SNAPSHOT_PATH", "data/snapshots/words_list_radix_words.json")


def save_words_list_snapshot():
    total_words = words_list_radix.save_snapshot(snapshot_path)
    logger.info(f"Saved words_list radix snapshot with {total_words} words")


loaded_words = words_list_radix.load_snapshot(snapshot_path)
if loaded_words > 0:
    logger.info(f"Loaded words_list radix snapshot with {loaded_words} words")

@router.post("/add_list")
async def add():
    if len(words_list_radix.root.children) > 0:
        raise HTTPException(status_code=400, detail="Tree not empty")
    with open("data/br-utf8.txt", "r") as file:
        words_list = file.read().splitlines()

    i = 0
    for i, word in enumerate(words_list, start=1):
        words_list_radix.insert(word)
        if i % 50000 == 0:
            logger.info(f"{i} added words")

    words_list_radix.update_tree()
    save_words_list_snapshot()

    logger.info(f"{i} added words")
    return {"detail": f"{i} words added successfully"}


@router.post("/clear_tree")
async def clear_tree():
    words_list_radix.clear()
    save_words_list_snapshot()
    logger.info("Tree cleared")
    return {"detail": "Tree cleared successfully"}



@router.get("/matches/{word}")
async def matches(word: str):
    word = word.strip().lower()
    if len(word) < 3:
        return {"length": 0, "words": []}

    result = words_list_radix.matches(word)

    return {"length": len(result), "words": result}
