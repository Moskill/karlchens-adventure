# game/systems/savegame.py
import json, os
from ..models.state import GameState

SAVE_VERSION = 1

def save(path: str, state: GameState):
    data = {
        "version": SAVE_VERSION,
        "money": state.money,
        "fans": state.fans,
        "grid_size": list(state.grid_size),
        "buildings": [
            {"id": b.attraction_id, "size": list(b.size), "pos": list(b.top_left)}
            for b in state.buildings
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)  # Kann dict sein – absichtlich roh
    except FileNotFoundError:
        return None

def load_or_init(path: str) -> GameState:
    d = load(path)
    if not d:
        return GameState()  # Default-State
    # tolerant mappen
    gs = GameState(
        money=int(d.get("money", 500)),
        fans=int(d.get("fans", 10)),
        grid_size=tuple(d.get("grid_size", (20, 20))),
    )
    blds = []
    for b in d.get("buildings", []):
        try:
            from ..models.state import PlacedBuilding
            blds.append(PlacedBuilding(
                attraction_id=b["id"],
                size=tuple(b.get("size", (1,1))),
                top_left=tuple(b.get("pos", (0,0))),
            ))
        except Exception:
            pass
    gs.buildings = blds
    return gs
