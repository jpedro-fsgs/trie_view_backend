import logging
import os
from typing import Set
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from models.radix import RadixTree
from models.trie import Trie
import asyncio
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

active_connections: Set[WebSocket] = set()
snapshot_path = os.environ.get("PUBLIC_RADIX_SNAPSHOT_PATH", "data/snapshots/public_radix_words.json")
snapshot_debounce_seconds = float(os.environ.get("PUBLIC_RADIX_SNAPSHOT_DEBOUNCE_SECONDS", "30"))
public_snapshot_task: asyncio.Task | None = None

public_trie = Trie()
public_radix = RadixTree()

loaded_words = public_radix.load_snapshot(snapshot_path)
if loaded_words > 0:
    for word in public_radix.get_all_words():
        public_trie.insert(word)
    public_trie.update_tree()
    logger.info(f"Loaded public radix snapshot with {loaded_words} words")


def save_public_snapshot():
    total_words = public_radix.save_snapshot(snapshot_path)
    logger.info(f"Saved public radix snapshot with {total_words} words")


async def _save_public_snapshot_debounced():
    try:
        await asyncio.sleep(snapshot_debounce_seconds)
        save_public_snapshot()
    except asyncio.CancelledError:
        return


def schedule_public_snapshot():
    global public_snapshot_task

    if public_snapshot_task and not public_snapshot_task.done():
        public_snapshot_task.cancel()

    public_snapshot_task = asyncio.create_task(_save_public_snapshot_debounced())

app_password = os.environ.get("APP_PASSWORD")

logger.info(f"Password set" if app_password else "Password not set")


@router.post("/clear/{password}")
async def clear(password):
    if app_password != password:
        raise HTTPException(status_code=403, detail="Wrong password")

    public_trie.clear()
    public_radix.clear()
    save_public_snapshot()

    await live_tree(
        connections=active_connections,
        trie=public_trie.get_tree(),
        radix=public_radix.get_tree(),
    )


@router.post("/pause/{password}")
async def pause(password):
    if app_password != password:
        raise HTTPException(status_code=403, detail="Wrong password")

    public_trie.block_insertion ^= True
    public_radix.block_insertion ^= True

    return {"status": "blocked" if public_radix.block_insertion else "not blocked"}


@router.post("/add_list")
async def add_list():
    with open("data/words-to-add.txt", "r") as file:
        words_list = file.read().splitlines()

    for word in words_list[:150]:
        public_trie.insert(word)
        public_trie.update_tree()
        public_radix.insert(word)
        public_radix.update_tree()

        await live_tree(
            connections=active_connections,
            trie=public_trie.get_tree(),
            radix=public_radix.get_tree(),
        )

        await asyncio.sleep(0.1)  # Delay of 100ms

    schedule_public_snapshot()

    return {"detail": f"{len(words_list)} words added successfully"}


@router.delete("/delete/{word}")
async def delete(word):
    success = public_trie.remove(word) and public_radix.remove(word)

    if not success:
        raise HTTPException(status_code=404, detail="Word not found")

    save_public_snapshot()

    await live_tree(
        connections=active_connections,
        trie=public_trie.get_tree(),
        radix=public_radix.get_tree(),
    )


@router.get("/tree")
async def generate_tree():
    return {"trie": public_trie.get_tree(), "radix": public_radix.get_tree()}


async def live_tree(connections, trie, radix):

    for connection in list(connections):
        try:
            await connection.send_json(
                {"connectedUsers": len(connections), "trie": trie, "radix": radix}
            )
        except Exception:
            connections.remove(connection)


async def insert(word: str):
    if public_trie.block_insertion and public_radix.block_insertion:
        raise HTTPException(status_code=403, detail="Insertion is currently blocked")

    public_trie.insert(word)
    public_trie.update_tree()
    public_radix.insert(word)
    public_radix.update_tree()
    schedule_public_snapshot()

    await live_tree(
        connections=active_connections,
        trie=public_trie.get_tree(),
        radix=public_radix.get_tree(),
    )


@router.post("/insert/{word}", status_code=201)
async def insert_post(word: str):
    word = word.strip().lower()
    if not word:
        raise HTTPException(status_code=400, detail="Empty word")
    if len(word) > 25:
        raise HTTPException(status_code=400, detail="Word too long")
    if " " in word:
        raise HTTPException(status_code=400, detail="Should be single word")

    await insert(word)


@router.get("/matches/{word}")
async def matches(word: str):
    word = word.strip().lower()

    result = public_radix.matches(word)

    return {"length": len(result), "words": result}


@router.websocket("/ws")
async def ws_connect(websocket: WebSocket):

    await websocket.accept()
    active_connections.add(websocket)
    logger.info(f"Usuários conectados: {len(active_connections)}")
    await websocket.send_json(
        {
            "connectedUsers": len(active_connections),
            "trie": public_trie.get_tree(),
            "radix": public_radix.get_tree(),
        }
    )

    try:
        await websocket.receive_text()

    except WebSocketDisconnect:
        # Desconexão normal do cliente
        logger.info(f"Cliente desconectou normalmente")
    except Exception as e:
        # Log de outros erros inesperados
        logger.info(f"Erro na conexão WebSocket: {str(e)}")
    finally:
        active_connections.remove(websocket)
        logger.info(f"Usuários conectados: {len(active_connections)}")
