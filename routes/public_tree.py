from typing import Set
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from models.improved_trie import ImprovedTrie
from models.radix import RadixTree
from models.trie import Trie

router = APIRouter()

active_connections: Set[WebSocket] = set()

public_trie = Trie()
public_radix = RadixTree()
public_improved_trie = ImprovedTrie()


@router.post("/clear")
async def clear():
    public_trie.clear()
    public_radix.clear()

    await live_tree(
        connections=active_connections,
        trie=public_trie.get_tree(),
        radix=public_radix.get_tree(),
    )

@router.delete("/delete/{word}")
async def delete(word):
    success = public_trie.remove(word) and public_radix.remove(word)

    if not success:
        raise HTTPException(status_code=404, detail="Word not found")
    
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

    public_trie.insert(word)
    public_radix.insert(word)

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


@router.websocket("/ws")
async def ws_connect(websocket: WebSocket):

    await websocket.accept()
    active_connections.add(websocket)
    print(f"Usuários conectados: {len(active_connections)}")
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
        print(f"Cliente desconectou normalmente")
    except Exception as e:
        # Log de outros erros inesperados
        print(f"Erro na conexão WebSocket: {str(e)}")
    finally:
        active_connections.remove(websocket)
        print(f"Usuários conectados: {len(active_connections)}")
