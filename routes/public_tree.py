from typing import Set
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from models.radix import RadixTree
from models.trie import Trie

router = APIRouter()

active_tree_connections: Set[WebSocket] = set()

public_trie = Trie()
public_radix = RadixTree()

@router.post("/clear")
async def clear():
    public_trie.clear()


@router.get("/tree")
async def generate_tree():
    return public_trie.get_tree

@router.post("/insert/{word}")
async def insert(word: str):
    word = word.strip().lower()
    if not word:
        raise HTTPException(status_code=400, detail="Empty word")
    if len(word) > 25:
        raise HTTPException(status_code=400, detail="Word too long")
    if " " in word:
        raise HTTPException(status_code=400, detail="Should be single word")

    public_trie.insert(word)


    await live_tree(connections=active_tree_connections, tree=public_trie.get_tree(), type="Trie")

    return {"status": "success"}


async def live_tree(connections, tree, type):

    for connection in list(connections):
        try:
            await connection.send_json({
                "type": type,
                "connected_users": len(connections),
                "tree": tree
            })
        except Exception:
            connections.remove(connection)


@router.websocket("/ws")
async def ws_connect(websocket: WebSocket):

    await websocket.accept()
    active_tree_connections.add(websocket)
    print(f"Usuários conectados: {len(active_tree_connections)}")
    await websocket.send_json({
                "type": "Trie",
                "connected_users": len(active_tree_connections),
                "tree": public_trie.get_tree()
            })

    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        # Desconexão normal do cliente
        print(f"Cliente desconectou normalmente")
    except Exception as e:
        # Log de outros erros inesperados
        print(f"Erro na conexão WebSocket: {str(e)}")
    finally:
        active_tree_connections.remove(websocket)
        print(f"Usuários conectados: {len(active_tree_connections)}")